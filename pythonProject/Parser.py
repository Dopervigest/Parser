import json
import requests
from bs4 import BeautifulSoup
from book import Book
from Out import out


def universal(user_search):
    f = open('Database.json')
    data = json.load(f)
    for i in data['site_info']:
        URL = i["URL"] + user_search +i["URL2"]
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(i["RESULTS"], class_=i["RESULTS2"])
        try:
            book_elements = results.find_all(i["BOOK_ELEMENTS"], class_=i["BOOK_ELEMENTS2"])
        except:
            continue

        for book_element in book_elements:
            title = book_element.find(i["TITLE"], class_=i["TITLE2"])
            author = book_element.find(i["AUTHOR"], class_=i["AUTHOR2"])
            price = book_element.find(i["PRICE"], class_=i["PRICE2"])
            link = book_element.find(i["LINK"], class_ =i["LINK2"])

            if title is None or title == "":
                continue
            else:
                title = title.text.strip()

            if author is None:
                author = ""
            else:
                author = author.text.strip()

            if price is None:
                price = book_element.find(i["PRICE"], class_=i["PRICE3"])
                if price is None:
                    continue
            else:
                price = str(price.text.strip()).replace(' руб.', '')

            link = str((i["LINK3"] + str(link.get('href'))))

            b = Book(title, author, price, link)
            Book.list_of_books.append(b)

    BookList = out()
    return(BookList)
