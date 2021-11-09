import requests
from bs4 import BeautifulSoup
import urllib.parse
query = 'Hellö Wörld@Python'
urllib.parse.quote(query)
print(urllib.parse.quote(query))

"""
search = input("Какую книгу вы хотите найти?:   ").replace(" ", "+")
URL = "https://fkniga.ru/search/?q=" + search
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("div", class_="category-cards-container js-catalog-content")
if not results:
    print("По вашему запросу ничего не нашлось")
else:
    book_elements = results.find_all("div", class_="grid__item columnDesktop--3 columnSmallDesktop--4 columnTablet--4 columnMobile--12")
    count = 1
    for book_element in book_elements:
        title = book_element.find("a", class_="card__title")
        author = book_element.find("div", class_="card__subtitle")
        price = book_element.find("div", class_="price price--ruble")
        link = book_element.find("a")
        print(count)
        count += 1
        print("Название:", title.text.strip())
        print("Автор:", author.text.strip())
        print("Цена:", price.text.strip())
        print("Ссылка:" , "https://fkniga.ru", link.get('href'), sep="")
        print()
"""""