from email.utils import formataddr
from smtp.smtp import EmailMessage


if __name__ == '__main__':
    from_address = ""
    to_address = ""
    subject = ""
    body = ""
    msg = EmailMessage(
        from_addr=from_address,
        to_addr=to_address,
        subject=subject,
        body=body,
    )

    from smtp.smtp import SMTP

    smtp = SMTP(
        host='smtp_server',
        port=587,
        debug=True,
    )

    smtp.start_tls()
    smtp.login('login', 'password')
    smtp.send_mail('example@mail.com', 'to_addr@mail.com', msg)
    smtp.quit()
    