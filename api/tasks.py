import base64
from email.mime.image import MIMEImage

from celery import shared_task
from django.core.mail import EmailMessage

from cherry.settings import EMAIL_HOST_USER

BODY_EMAIL = 'Email пользователя: {}, Cообщение: {}'
SUBJECT_EMAIL = 'Обращение от пользователя {}'


@shared_task
def send_feedback_email(name, email, message, image_file=None):
    email = EmailMessage(
        subject=SUBJECT_EMAIL.format(name),
        body=BODY_EMAIL.format(email, message),
        from_email=EMAIL_HOST_USER,
        to=[EMAIL_HOST_USER],
    )
    if image_file:
        format, imgstr = image_file.split(';base64,')
        ext = format.split('/')[-1]
        file = MIMEImage(base64.b64decode(imgstr), name=f'image.{ext}', _subtype=ext)
        email.attach(file)
    email.send(fail_silently=False)
