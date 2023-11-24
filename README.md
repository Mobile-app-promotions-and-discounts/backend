# backend
backend для мобильного приложения управления скидками "Черри"

Для того, чтобы запустить приложение локально:
- Переименуйте файл .`env.example`(backend/cherry) в `.env` и подставьте свои данные
- Примените зависимости командой `pip install -r requirements.txt`
- Создать миграции `python manage.py makemigrations`
- Примените миграции `python manage.py migrate`
- Запустите сервер разработки `python manage.py runserver`
