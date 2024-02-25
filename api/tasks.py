import base64
from celery import shared_task
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage

from cherry.settings import EMAIL_HOST_USER


@shared_task
def send_email(name: str, email: str, message: str, image_file=None) -> None:
    email = EmailMessage(
        subject=f'Обратная связь от пользователя {name}',
        body=f'Email пользователя: {email}, Cообщение: {message}',
        from_email=EMAIL_HOST_USER,
        to=[EMAIL_HOST_USER],
    )
    if image_file:
        format, imgstr = image_file.split(';base64,')
        ext = format.split('/')[-1]
        file = MIMEImage(base64.b64decode(imgstr), name=f'image.{ext}', _subtype=ext)
        email.attach(file)
    email.send(fail_silently=False)
