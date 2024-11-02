from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Optional

from .settings import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_DAYS = 5


def create_confirmation_token(email: str) -> str:
    """
    Создает JWT с заданными данными и временем истечения.

    :param email: email, которыйй нужно закодировать в токен.
    :return: Закодированный JWT.
    """
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)  
    to_encode = {'sub': email, 'exp': expire}
    encode_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)  
    return encode_jwt

def verify_confirmation_token(token: str) -> Optional[str]:
    """
    Проверяет JWT и возвращает email, если токен действителен, иначе None.
    
    :param token: JWT для проверки.
    :return: email, если токен действителен, иначе None.
    """
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            return None
        return email
    except JWTError:
        return None

class SMTPClient:
    def __init__(self, host, port, user, password, use_tls=True):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.use_tls = use_tls
        self.from_email = settings.SMTP.DEFAULT_FROM_EMAIL

    def connect(self):
        self.server = SMTP(self.host, self.port)
        self.server.set_debuglevel(1)
        if self.use_tls:
            self.server.starttls()
        self.server.login(self.user, self.password)

    def _prepare_message(self, to_email: str, subject: str, body: str) -> MIMEMultipart:
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        return msg
    
    def _send_mail(self, to_email: str, subject: str, body: str):
        msg: MIMEMultipart = self._prepare_message(to_email, subject, body)
        self.server.sendmail(
            from_addr=self.from_email,
            to_addrs=to_email,
            msg=msg.as_bytes()
        )
        return msg

    def send_email(self, to_email: str, subject: str, body: str):
        try:
            self.connect()
            self._send_mail(to_email, subject, body)
        except Exception as e:
            print(e)
        finally:
            self.close()

    def close(self):
        if self.server:
            self.server.quit()


client = SMTPClient(
    host=settings.SMTP.HOST,
    port=settings.SMTP.PORT,
    user=settings.SMTP.USER,
    password=settings.SMTP.PASSWORD,
    use_tls=settings.SMTP.USE_TLS,
)