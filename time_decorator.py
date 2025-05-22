import time
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f'Функция выполнилась за {elapsed_time} секунд')
        return function
    return wrapper
