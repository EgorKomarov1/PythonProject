import requests
from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

"""
TODO:
1. Добавить логирование с использованием logging (заместо Print)
2. Разобраться что такое декоратор, try/except вынести в декоратор
3. Выводить в консоль (с помощью print) нужно в основном только на дебаге кода 
    изучи вопрос куда можно сохранять полученные данные (какие БД существуют, 
    какие форматы файлов существуют для хранения данных)
4. Нужно изучить, что такое requerments и создать его в проекте
5. Нужно изучить, что такое gitignore и создать его в проекте 

"""


def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Ошибка в функции {func.__name__}: {e}")
            return None
    return wrapper


@try_except_decorator
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
    adres = soup.find('div', class_='contacts__text')
    if adres:
        adres_ur = adres.get_text(strip=True)
        logging.info(f'Адрес: {adres_ur[27:]}')

    # Директор
    director_div = soup.find('div', class_='user__name')
    if director_div:
        director_name = director_div.get_text(strip=True)
        raw_name = re.sub(r"(?<=\w)([А-ЯЁ])", r" \1", director_name)
        logging.info(f'Директор: {raw_name}')

        # Завучи
    logging.info('\n Завучи:')

    # TODO код повторяется, отличии минимальны, соблюдай принцип DRY и в соответствии с этим принципом внеси изменения в код
    # region переписать по DRY
    fa_zam_ruk = ['/kop', '/evs', '/cur', '/sem', '/sta']
    zam_ruk = soup.find_all('a', class_='menu__link', href=lambda x: x and any(x.startswith(p) for p in fa_zam_ruk))
    if zam_ruk:
        for a in zam_ruk:
            logging.info(f'{a.get_text(strip=True)}')
    # endregion

    # Новости
    logging.info("\n Ссылки на новости:")
    news_links = set()

    for block in soup.find_all(class_=re.compile('news', re.IGNORECASE)):
        for a in block.find_all('a', href=True):
            link = a['href']
            if not link.startswith(('javascript:', '#')):
                news_links.add(link if link.startswith('http') else f"{url.rstrip('/')}/{link.lstrip('/')}")

    for a in soup.find_all('a', href=True, string=re.compile('news', re.IGNORECASE)):
        link = a['href']
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
