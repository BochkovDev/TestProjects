import socket
import sys
import datetime
import ssl
from typing import (
    Optional,
    Tuple,
    Callable,
)
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.base64mime import body_encode as encode_base64
from email.base64mime import body_decode as decode_base64

from .utils import quoteaddr, addr_only, fix_eols, quote_periods
from .typing import SMTPStatusCode


SMTP_PORT = 25
SMTP_TLS_PORT = 465
CRLF = '\r\n'
bCRLF = b'\r\n'
SMTP_START_TLS_PORT = 587
DEFAULT_TIMEOUT = 60
_MAXLINE = 8192
_MAXCHALLENGE = 5


class SMTPException(OSError):
    """Base class for all exceptions raised by this module."""

class SMTPNotSupportedError(SMTPException):
    """The command or option is not supported by the SMTP server.

    This exception is raised when an attempt is made to run a command or a
    command with an option which is not supported by the server.
    """

class SMTPServerDisconnected(SMTPException):
    """Not connected to any SMTP server.

    This exception is raised when the server unexpectedly disconnects,
    or when an attempt is made to use the SMTP instance before
    connecting it to a server.
    """

class SMTPResponseException(SMTPException):
    """Base class for all exceptions that include an SMTP error code.

    These exceptions are generated in some instances when the SMTP
    server returns an error code.  The error code is stored in the
    `smtp_code' attribute of the error, and the `smtp_error' attribute
    is set to the error message.
    """

    def __init__(self, code, msg):
        self.smtp_code = code
        self.smtp_error = msg
        self.args = (code, msg)

class SMTPSenderRefused(SMTPResponseException):
    """Sender address refused.

    In addition to the attributes set by on all SMTPResponseException
    exceptions, this sets `sender' to the string that the SMTP refused.
    """

    def __init__(self, code, msg, sender):
        self.smtp_code = code
        self.smtp_error = msg
        self.sender = sender
        self.args = (code, msg, sender)

class SMTPRecipientsRefused(SMTPException):
    """All recipient addresses refused.

    The errors for each recipient are accessible through the attribute
    'recipients', which is a dictionary of exactly the same sort as
    SMTP.sendmail() returns.
    """

    def __init__(self, recipients):
        self.recipients = recipients
        self.args = (recipients,)


class SMTPDataError(SMTPResponseException):
    """The SMTP server didn't accept the data."""

class SMTPConnectError(SMTPResponseException):
    """Error during connection establishment."""

class SMTPHeloError(SMTPResponseException):
    """The server refused our HELO reply."""

class SMTPAuthenticationError(SMTPResponseException):
    """Authentication error.

    Most probably the server didn't accept the username/password
    combination provided.
    """


class EmailMessage:
    def __init__(self, from_addr: str = '', to_addr: str = '', subject: str = '', body: str = '', headers: dict = {}) -> None:
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.subject = subject
        self.body = body
        self.headers = headers

    def _prepare_message(self) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg['From'] = formataddr((self.from_addr, self.from_addr))
        msg['To'] = formataddr((self.to_addr, self.to_addr))
        msg['Subject'] = self.subject

        for key, value in self.headers.items():
            msg[key] = value

        msg.attach(MIMEText(self.body, 'plain'))
        return msg
    
    def as_string(self) -> str:
        msg = self._prepare_message()
        return msg.as_string()
    
    def as_bytes(self) -> bytes:
        msg = self._prepare_message()
        return msg.as_bytes()

    def __bytes__(self) -> bytes:
        return self.as_bytes()


class SMTP:
    debug = False

    sock = None
    file = None
    helo_resp = None
    default_port = SMTP_PORT
    command_encoding = 'ascii'

    def __init__(
        self,
        *,
        host: Optional[str] = None,
        port: Optional[int] = None,
        local_hostname: Optional[str] = None,
        source_address: Optional[Tuple[str, int]] = None,
        timeout: Optional[float] = DEFAULT_TIMEOUT,
        debug: bool = False,
    ) -> None:
        self.host = host
        self.port = port
        self.source_address = source_address
        self.timeout = timeout
        self.debug = debug

        if host:
            self.connect(host, port)

        if local_hostname is not None:
            self.local_hostname = local_hostname
        else:
            fqdn = socket.getfqdn()
            if '.' in fqdn:
                self.local_hostname = fqdn
            else:
                addr = '127.0.0.1'
                try:
                    addr = socket.gethostbyname(socket.gethostname())
                except socket.gaierror:
                    pass
                self.local_hostname = '[%s]' % addr

    def _connect(self, host: str, port: int, timeout: int):
        if timeout is not None and not timeout:
            raise ValueError('Timeout=0 not supported')
        return socket.create_connection(
            address=(host, port),
            timeout=timeout,
            source_address=self.source_address,
        )
    
    def set_debug(self, option: bool) -> None:
        self.debug = option
    
    def _print_debug(self, *args):
        if self.debug == True:
            print(datetime.datetime.now().time(), *args, file=sys.stderr)
        else:
            print(*args, file=sys.stderr)

    def connect(self, host='localhost', port=0, source_address=None) -> Tuple[SMTPStatusCode, bytes]:
        if source_address:
            self.source_address = source_address

        if not port and (host.find(':') == host.rfind(':')):
            i = host.rfind(':')
            if i >= 0:
                host, port = host[:i], host[i+1:]
                try: 
                    port = int(port)
                except ValueError:
                    raise OSError('Nonnumeric port')
        if not port:
            port = self.default_port

        self.sock = self._connect(host, port, self.timeout)
        code, msg = self.get_reply()
        return (code, msg)
    
    def send(self, s: str) -> None:
        if self.sock:
            if isinstance(s, str):
                s = s.encode(self.command_encoding)
            try:
                self.sock.sendall(s)
                if self.debug:
                    self._print_debug('H: %s' % s)
            except OSError:
                self.close()
                raise SMTPServerDisconnected('Server not connected')
        else:
            raise SMTPServerDisconnected('please run connect() first')

    def put_cmd(self, cmd: str, args='') -> None:
        if args == '':
            s = cmd
        else:
            s = f'{cmd} {args}'
        if '\r' in s or '\n' in s:
            s = s.replace('\n', '\\n').replace('\r', '\\r')
            raise ValueError(
                f'command and arguments contain prohibited newline characters: {s}'
            )
        self.send(f'{s}{CRLF}')

    def do_cmd(self, cmd: str, args='') -> Tuple[SMTPStatusCode, bytes]:
        self.put_cmd(cmd, args)
        return self.get_reply()
        
    def get_reply(self) -> Tuple[SMTPStatusCode, bytes]:
        resp = []

        if self.file is None:
            self.file = self.sock.makefile('rb')

        while True:
            try:
                line = self.file.readline(_MAXLINE + 1)
            except OSError as e:
                self.close()
                raise SMTPServerDisconnected("Connection unexpectedly closed: " + str(e))
            if not line:
                self.close()
                raise SMTPServerDisconnected("Connection unexpectedly closed")
            if len(line) > _MAXLINE:
                self.close()
                raise SMTPResponseException(500, "Line too long.")
            resp.append(line[4:].strip(b' \t\r\n'))
            code = line[:3]
            try:
                code = SMTPStatusCode(int(code))
            except ValueError:
                code = SMTPStatusCode.INVALID_RESPONSE
                break
            if line[3:4] != b'-':
                break
        
        msg = b'\n'.join(resp)
        if self.debug:
            self._print_debug('S: %i %s' % (code, msg))
        return (code, msg)
    
    def helo(self, name=''):
        self.put_cmd('HELO', name or self.local_hostname)
        (code, msg) = self.get_reply()
        self.helo_resp = msg
        return (code, msg)
    
    def helo_if_needed(self):
        if self.helo_resp is None:
            (code, msg) = self.helo()
            if not (200 <= code <= 299):
                raise SMTPHeloError(code, msg)
    
    def auth(self, mechanism: str, authobject: Callable, *, initial_response_ok=True):
        mechanism = mechanism.upper()
        initial_response = (authobject() if initial_response_ok else None)
        if initial_response is not None:
            response = encode_base64(initial_response.encode('ascii'), eol='')
            (code, msg) = self.do_cmd('AUTH', mechanism + ' ' + response)
            self._auth_challenge_count = 1
        else:
            (code, msg) = self.do_cmd('AUTH', mechanism)
            self._auth_challenge_count = 0
        while code == SMTPStatusCode.SERVER_CHALLENGE:
            self._auth_challenge_count += 1
            challenge = decode_base64(msg)
            response = encode_base64(authobject(challenge).encode('ascii'), eol='')
            (code, msg) = self.do_cmd(response)
            if self._auth_challenge_count > _MAXCHALLENGE:
                raise SMTPException(
                    "Server AUTH mechanism infinite loop. Last response: " + repr((code, msg))
                ) 
        if code in (SMTPStatusCode.AUTHENTICATION_SUCCESS, SMTPStatusCode.BAD_SEQUENCE):
            return (code, msg)
        raise SMTPAuthenticationError(code, msg)

    def auth_plain(self, challenge=None):
        return "\0%s\0%s" % (self.user, self.password)

    def auth_login(self, challenge=None):
        if challenge is None or self._auth_challenge_count < 2:
            return self.user
        else:
            return self.password

    def login(self, user, password, *, initial_response_ok=True):
        self.helo_if_needed()

        auth_list = ['PLAIN', 'LOGIN']

        self.user, self.password = user, password
        for auth_method in auth_list:
            method_name = 'auth_' + auth_method.lower().replace('-', '_')
            try:
                (code, resp) = self.auth(
                    auth_method, getattr(self, method_name),
                    initial_response_ok=initial_response_ok)
                if code in (SMTPStatusCode.AUTHENTICATION_SUCCESS, SMTPStatusCode.BAD_SEQUENCE):
                    return (code, resp)
            except Exception as e:
                last_exception = e
        raise last_exception

    def starttls(self, keyfile=None, certfile=None, context=None):
        self.helo_if_needed()
        (code, msg) = self.do_cmd("STARTTLS")
        if code == SMTPStatusCode.SERVICE_READY:
            if context is not None and keyfile is not None:
                raise ValueError("context and keyfile arguments are mutually "
                                 "exclusive")
            if context is not None and certfile is not None:
                raise ValueError("context and certfile arguments are mutually "
                                 "exclusive")
            if keyfile is not None or certfile is not None:
                import warnings
                warnings.warn("keyfile and certfile are deprecated, use a "
                              "custom context instead", DeprecationWarning, 2)
            if context is None:
                context = ssl._create_stdlib_context(certfile=certfile, keyfile=keyfile)
            self.sock = context.wrap_socket(self.sock, server_hostname=self.host)
            self.file = None
            self.helo_resp = None
        else:
            raise
        return (code, msg)
        
    def rset(self):
        self.command_encoding = 'ascii'
        return self.do_cmd('RSET')
    
    def noop(self):
        return self.do_cmd('NOOP')
    
    def mail(self, sender: str, options=()):
        self.put_cmd('MAIL', 'FROM:%s' % (quoteaddr(sender)))
        return self.get_reply()
    
    def help(self, args=''):
        self.put_cmd('HELP', args)
        (code, msg) = self.get_reply()
        return (code, msg)
    
    def mail(self, sender, options=()):
        option_list = ''
        if options:
            option_list = ' '.join(options)
        self.put_cmd('MAIL', 'FROM:%s %s' % (quoteaddr(sender), option_list))
        return self.get_reply()
    
    def data(self, msg: EmailMessage):
        self.put_cmd('DATA')
        (code, resp) = self.get_reply()
        if code != SMTPStatusCode.START_MAIL_INPUT:
            raise SMTPDataError(code, resp)
        else:
            if isinstance(msg, str):
                msg = fix_eols(msg).encode('ascii')
            q = quote_periods(msg.as_bytes())
            if q[-2:] != bCRLF:
                q = q + bCRLF
            q = q + b"." + bCRLF
            self.send(q)
            (code, msg) = self.get_reply()
            return (code, msg)
    
    def rcpt(self, recip, options=()):
        self.put_cmd('RCPT', 'TO:%s' % (quoteaddr(recip)))
        return self.get_reply()
    
    def verify(self, address):
        self.put_cmd('VRFY', addr_only(address))
        return self.get_reply()
    
    def send_mail(self, from_addr, to_addrs, msg: EmailMessage):
        self.helo_if_needed()
        if isinstance(msg, str):
            msg = fix_eols(msg).encode('ascii')
        (code, _) = self.mail(from_addr)
        if code != SMTPStatusCode.COMPLETED:
            if code == SMTPStatusCode.SERVICE_NOT_AVAILABLE:
                self.close()
            else:
                self.rset()
            raise SMTPSenderRefused(code, msg, from_addr)
        senderrs = {}
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        for recip in to_addrs:
            (code, resp) = self.rcpt(recip)
            if (code != SMTPStatusCode.COMPLETED) and (code != SMTPStatusCode.USER_NOT_LOCAL):
                senderrs[recip] = (code, resp)
            if code == SMTPStatusCode.SERVICE_NOT_AVAILABLE:
                self.close()
                raise SMTPRecipientsRefused(senderrs)
        if len(senderrs) == len(to_addrs):
            self.rset()
            raise SMTPRecipientsRefused(senderrs)
        (code, resp) = self.data(msg)
        if code != SMTPStatusCode.COMPLETED:
            if code == SMTPStatusCode.SERVICE_NOT_AVAILABLE:
                self.close()
            else:
                self.rset()
            raise SMTPDataError(code, resp)
        return senderrs

    def start_tls(self, keyfile=None, certfile=None, context=None):
        self.helo_if_needed()
        (code, msg) = self.do_cmd('STARTTLS')
        if code == SMTPStatusCode.SERVICE_READY:
            context = ssl._create_stdlib_context(certfile=certfile, keyfile=keyfile)
            self.sock = context.wrap_socket(self.sock, server_hostname=self.host)
            self.file = None
            self.helo_resp = None
        return (code, msg)

    def close(self):
        try:
            file = self.file
            self.file = None
            if file:
                file.close()
        finally:
            sock = self.sock
            self.sock = None
            if sock:
                sock.close()

    def quit(self):
        res = self.do_cmd('QUIT')
        self.close()
        return res