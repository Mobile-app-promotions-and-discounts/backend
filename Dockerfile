FROM python:3.10-slim
WORKDIR /cherry_app
COPY requirements.txt /cherry_app
RUN pip3 install -r /cherry_app/requirements.txt --no-cache-dir
COPY . /cherry_app
CMD ["gunicorn", "cherry.wsgi:application", "--bind", "0:8000"] 
