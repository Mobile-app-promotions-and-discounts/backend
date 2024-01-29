from datetime import datetime
from functools import wraps


def calc_time_work(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        start = datetime.today()
        print(f'{func} начала работу в {start}')
        result = func(*args, **kwargs)
        print(f'Функция {func} закончила работу за {datetime.today() - start}')
        return result
    return wraper
