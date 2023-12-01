# Описание проекта
API для мобильного приложения управления скидками "Черри".

### Технологии, которые использовались при разработке проекта
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python](https://www.python.org/)
- [Django Framework](https://www.djangoproject.com/)

### Как запустить приложение локально:
- Переименуйте файл .`env.example`(backend/cherry) в `.env`
- Добавьте свои данные для переменных в secrets:
```
SECRET_KEY='string'
DEBUG=False
ALLOWED_HOSTS=127.0.0.1, 0.0.0.0, web, localhost
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
DB_HOST=db_host
DB_PORT=5432
HOST=IP_host
```


- Примените зависимости командой `pip install -r requirements.txt`
- Создайте миграции `python manage.py makemigrations`
- Примените миграции `python manage.py migrate`
- Запустите сервер разработки `python manage.py runserver`

### Над проектом работали:
* Роман Буцких https://github.com/BnamoRS
* Валерия Малышева https://github.com/valerycode
* Савелий Худяк https://github.com/rakikz
* Арина Сухова https://github.com/sukhovarina
* Наталья Арлазарова https://github.com/sic15
