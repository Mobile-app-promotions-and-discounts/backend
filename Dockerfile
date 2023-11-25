FROM python:3.10-slim

# Запустить команду создания директории внутри контейнера
RUN mkdir /cherry_app

# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY requirements.txt /cherry_app

# Выполнить установку зависимостей внутри контейнера.
RUN pip3 install -r /cherry_app/requirements.txt --no-cache-dir

# Скопировать содержимое директории /api_yamdb c локального компьютера
# в директорию /app.
COPY . /cherry_app

# Сделать директорию /app рабочей директорией. 
WORKDIR /cherry_app

# RUN python3 manage.py migrate

# Выполнить запуск сервера разработки при старте контейнера.
CMD ["python3", "manage.py", "runserver", "0:8000"] 