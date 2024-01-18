FROM python:3.10

WORKDIR /code

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod a+x ./run_scr_lenta.sh
