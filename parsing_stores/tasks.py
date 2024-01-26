from cherry.celery import app


@app.task
def run_src_lenta():
    print(f'ТАСКА ТАСКА ТАСКА ТАСКА ПАРСИМ ЛЕНТ ЛЕНТУ {str}')
