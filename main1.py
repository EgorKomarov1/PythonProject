import requests
from bs4 import BeautifulSoup
import re
import logging
import time

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("errors.log")
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


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


@try_except_decorator
@time_decorator
def parse_gymnasium_19(url):
    # Запрос к сайту
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Контакты
    logging.info("\n Контактные данные:")

    # Телефон
    phone_link = soup.find('a', class_='departments__link', href=lambda x: x and x.startswith('tel:'))
    if phone_link:
        phone_numbers = phone_link.get_text(strip=True)
        logging.info(f'Телефон: {phone_numbers}')

        # Email
    email = soup.find('a', href=lambda x: x and x.startswith('mailto:'))
    if email:
        email_ = email.get_text(strip=True)
        logging.info(f'Email: {email_}')
    # Адрес
    address = soup.find('div', class_='contacts__text')
    if address:
        address_ur = address.get_text(strip=True)
        logging.info(f'Адрес: {address_ur[27:]}')

    # Директор
    director_div = soup.find('div', class_='user__name')
    if director_div:
        director_name = director_div.get_text(strip=True)
        raw_name = re.sub(r"(?<=\w)([А-ЯЁ])", r" \1", director_name)
        logging.info(f'Директор: {raw_name}')

    # Завучи
    logging.info('\n Завучи:')

    all_lastnames_headteacher = ['/kop', '/evs', '/cur', '/sem', '/sta']
    headteachers = soup.find_all('a', class_='menu__link', href=lambda x: x and any(x.startswith(p) for p in
                                                                                    all_lastnames_headteacher))
    if headteachers:
        for lastname_headteacher in headteachers:
            logging.info(f'{lastname_headteacher.get_text(strip=True)}')

    # Новости
    logging.info("\n Ссылки на новости:")
    news_links = set()

    for block in soup.find_all(class_=re.compile('news', re.IGNORECASE)):
        for news in block.find_all('a', href=True):
            link = news['href']
            if not link.startswith(('javascript:', '#')):
                news_links.add(link if link.startswith('http') else f"{url.rstrip('/')}/{link.lstrip('/')}")
    # Вывод
    if news_links:
        for link in news_links:
            logging.info(f"{link}")
    else:
        logging.info("Не найдено.")


if __name__ == "__main__":
    website_url = "https://orel-gym19.obr57.ru/"
    parse_gymnasium_19(website_url)
