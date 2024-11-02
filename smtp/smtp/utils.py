import re
from email.utils import parseaddr


CRLF = '\r\n'

def quoteaddr(addrstring: str):
    displayname, addr = parseaddr(addrstring)
    if (displayname, addr) == ('', ''):
        if addrstring.strip().startswith('<'):
            return addrstring
        return "<%s>" % addrstring
    return "<%s>" % addr

def addr_only(addrstring):
    displayname, addr = parseaddr(addrstring)
    if (displayname, addr) == ('', ''):
        return addrstring
    return addr

def quote_periods(bindata):
    return re.sub(br'(?m)^\.', b'..', bindata)

def fix_eols(data):
    return  re.sub(r'(?:\r\n|\n|\r(?!\n))', CRLF, data)