# backend
backend для мобильного приложения управления скидками "Черри"

Для того, чтобы запустить приложение локально:
- Переименуйте файл .`env.example`(backend/cherry) в `.env` и подставьте свои данные
- Примените зависимости командой `pip install -r requirements.txt`
- Примените миграции `python manage.py migrate`
- Запустите сервер разработки `python manage.py runserver`

Зависимости:

Django==4.2.7
django-filter==23.3
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
djoser==2.2.2
Pillow==10.1.0
python-dotenv==1.0.0

