import os
from django.core.mail import send_mail

CHERRY_EMAIL = os.environ.get('CHERRY_EMAIL')


def send_email(name='', email='tyrtychnyy90@mail.ru', message=''):
    send_mail(
        'Обратная связь от пользователя',
        f'Имя пользователя: {name},'
        f'email пользователя: {email},'
        f'сообщение: {message}',
        CHERRY_EMAIL,
        [CHERRY_EMAIL],
        fail_silently=False,
    )
