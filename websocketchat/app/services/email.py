from core.email import client, create_confirmation_token



def send_email_with_verification_link(abs_url: str, to_email: str):
    token = create_confirmation_token(to_email)
    url = f'{abs_url}?token={token}'
    subject = 'Подтверждение создания аккаунта'
    return client.send_email(to_email, subject, url)
