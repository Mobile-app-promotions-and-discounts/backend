# backend
backend для мобильного приложения управления скидками "Черри"

Для того, чтобы запустить приложение локально:
- Переименуйте файл .`env.example`(backend/cherry) в `.env` и подставьте свои данные
- Примените зависимости командой `pip install -r requirements.txt`
- Примените миграции `python manage.py migrate`
- Запустите сервер разработки `python manage.py runserver`

Зависимости:

asgiref==3.7.2
Django==4.2.7
django-filter==23.3
djangorestframework==3.14.0
pytz==2023.3.post1
sqlparse==0.4.4
typing_extensions==4.8.0

