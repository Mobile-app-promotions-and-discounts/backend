from datetime import datetime
from functools import wraps


def calc_time_work(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        start = datetime.today()
        print(f'{func} начала работу в {start}')
        result = func(*args, **kwargs)
        time_work = datetime.today() - start
        print(f'Функция {func} закончила работу за {time_work}')
        return result
    return wraper
