import openpyxl as opxl
import requests
from bs4 import BeautifulSoup
from book import Book
from Out import out
user_search = 'Гарри Поттер'


def universal():
    wb = opxl.load_workbook('./Data_Base.xlsx')
    sheet = wb['Data_Base']

    for i in range(2, 5):
        URL = sheet['A' + str(i)].value + user_search
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(sheet['C'+ str(i)].value, class_=sheet['D'+ str(i)].value)
        book_elements = results.find_all(sheet['E'+ str(i)].value, class_=sheet['F'+ str(i)].value)
        for book_element in book_elements:
            title = book_element.find(sheet['G' + str(i)].value, class_=sheet['H' + str(i)].value)
            author = book_element.find(sheet['I'+ str(i)].value, class_=sheet['J' + str(i)].value)
            price = book_element.find(sheet['K' + str(i)].value, class_=sheet['L' + str(i)].value)
            link = book_element.find(sheet['M' + str(i)].value)

            if title is None:
                continue
            else:
                title = title.text.strip()

            if author is None:
                author = ""
            else:
                author = author.text.strip()

            if price is None:
                continue
            else:
                price = str(price.text.strip()).replace(' руб.', '')

            link = str((sheet['O' + str(i)].value + str(link.get('href'))))

            b = Book(title, author, price, link)
            Book.list_of_books.append(b)

    out()

"""print(title.text.strip())
print(author.text.strip())
print(str(price.text.strip()).replace(' руб.', ''))
print(sheet['O2'].value + str(link.get('href')))"""


#universal()
