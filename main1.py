import requests
from bs4 import BeautifulSoup
import re

def parse_gymnasium_19(url):
    try:
        # Запрос к сайту
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Контакты ---
        print("\n Контакты:")

        # Телефоны (все возможные форматы)
        contact_section = soup.find("footer") or soup.find(class_="contacts") or soup
        text = contact_section.get_text()
        phone_regex = r'(?:\+7|8)[\s\-]?\(?\d{3,4}\)?[\s\-]?\d{2,3}[\s\-]?\d{2}[\s\-]?\d{2}'
        phones = set(re.findall(phone_regex, response.text))
        if phones:
            print("• Телефоны:", ", ".join([re.sub(r'\D', '', p) for p in phones]))

        # Email
        emails = set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', response.text))
        if emails:
            print("• Email:", ", ".join(emails))

        # Адрес
        address_keywords = ['адрес', 'address', 'ул.', 'улица', 'Орел', 'Орёл']
        address = None
        for keyword in address_keywords:
            found = soup.find(string=re.compile(keyword, re.IGNORECASE))
            if found:
                address = found.parent.get_text(" ", strip=True)
                break
        if address:
            print("• Адрес:", address)

        # --- Новости ---
        print("\n Ссылки на новости:")
        news_links = set()

        for block in soup.find_all(class_=re.compile(r'news|новости|post', re.IGNORECASE)):
            for a in block.find_all('a', href=True):
                link = a['href']
                if not link.startswith(('javascript:', '#')):
                    news_links.add(link if link.startswith('http') else f"{url.rstrip('/')}/{link.lstrip('/')}")

        for a in soup.find_all('a', href=True, string=re.compile(r'новости|news|события', re.IGNORECASE)):
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
