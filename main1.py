import requests
from bs4 import BeautifulSoup
import re

def parse_gymnasium_19(url):
    try:
        # Запрос к сайту
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Контакты
        print("\n Контакты:")

        # Телефон
        phone_link = soup.find('a', class_='departments__link', href=lambda x: x and x.startswith('tel:'))
        if phone_link:
            phone_numbers = phone_link.get_text(strip=True)
            print(f'• Телефон: {phone_numbers}')

        # Email
        email = soup.find('a',href=lambda x: x and x.startswith('mailto:'))
        if email:
            email_ = email.get_text(strip=True)
            print(f'• Email: {email_}')
        # Адрес
        adres = soup.find('div', class_='contacts__text')
        if adres:
            adres_ur = adres.get_text(strip=True)
            print(f'• Адрес: {adres_ur[27:]}')

        # Руководитель
        director_div = soup.find('div', class_='user__name')
        if director_div:
            director_name = director_div.get_text(strip=True)
            raw_name = re.sub(r"(?<=\w)([А-ЯЁ])", r" \1", director_name)
            print(f'• Руководитель: {raw_name}')

        # Новости
        print("\n Ссылки на новости:")
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
                print(f"→ {link}")
        else:
            print("Не найдено.")

    except Exception as e:
        print(f"Ошибка: {e}")

url = "https://orel-gym19.obr57.ru/"
if __name__ == "__main__":
    parse_gymnasium_19(url)
