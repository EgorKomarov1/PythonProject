import requests
from bs4 import BeautifulSoup
import re
from decorator import time_decorator, try_except_decorator, logging


@try_except_decorator
@time_decorator
def parse_gymnasium_19(url: str) -> None:
    """

    :param url: ссылка на сайт
    :return: телефон, email, адрес, ФИО директора, ФИО завучей, ссылки на последние 5 новостей
    """

    # Запрос к сайту

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Контакты
    logging.info("\n Контактные данные:")

    # Телефон
    def find_phone_numbers():
        phone_link = soup.find('a', class_='departments__link', href=lambda x: x and x.startswith('tel:'))
        if phone_link:
            phone_number = phone_link.get_text(strip=True)
            return phone_number
    logging.info(f'Номер телефона: {find_phone_numbers()}')

    # Email
    def find_email_address():
        email = soup.find('a', href=lambda x: x and x.startswith('mailto:'))
        if email:
            email_ = email.get_text(strip=True)
            return email_
    logging.info(f'Email: {find_email_address()}')

    # Адрес
    def find_address_school():
        address = soup.find('div', class_='contacts__text')
        if address:
            address_ur = address.get_text(strip=True)
            return address_ur[27:]
    logging.info(f'Адрес: {find_address_school()}')

    # Директор
    def find_director():
        director_div = soup.find('div', class_='user__name')
        if director_div:
            director_name = director_div.get_text(strip=True)
            raw_name = re.sub(r"(?<=\w)([А-ЯЁ])", r" \1", director_name)
            return raw_name
    logging.info(f'Директор: {find_director()}')

    # Завучи
    logging.info('\n Завучи:')

    def find_headteachers():
        all_lastnames_headteachers = ['/kop', '/evs', '/cur', '/sem', '/sta']
        headteachers = soup.find_all('a', class_='menu__link', href=lambda x: x and any(x.startswith(p) for p in
                                                                                        all_lastnames_headteachers))
        if headteachers:
            for FCs_headteacher in headteachers:
                logging.info(f'{FCs_headteacher.get_text(strip=True)}')
    find_headteachers()

    # Новости
    logging.info("\n Ссылки на новости:")
    news_links = set()

    def find_last_news_links():
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
    find_last_news_links()


if __name__ == "__main__":
    website_url = "https://orel-gym19.obr57.ru/"
    parse_gymnasium_19(website_url)
