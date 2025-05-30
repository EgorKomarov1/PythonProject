from logger import logger, logging
import time


def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            function = func(*args, **kwargs)
            return function
        except Exception as e:
            logger.error(f"Ошибка в функции: {e}", exc_info=True)
            return None
    return wrapper


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f'Функция выполнилась за {elapsed_time} секунд')
        return function
    return wrapper
