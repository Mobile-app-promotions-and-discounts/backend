from celery import shared_task
from django.core.mail import send_mail

from cherry.settings import EMAIL_HOST_USER


@shared_task
def send_email(email, name, message):
    send_mail(
        'Обратная связь от пользователя',
        f'Имя пользователя: {name}, '
        f'Email пользователя: {email}, '
        f'Cообщение: {message}',
        EMAIL_HOST_USER,
        [EMAIL_HOST_USER],
        fail_silently=False,
    )
