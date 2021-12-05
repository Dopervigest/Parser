import openpyxl as opxl
import requests
from bs4 import BeautifulSoup
from book import Book
from Out import out
user_search = 'Гарри Поттер'


def universal():
    wb = opxl.load_workbook('./Data_Base.xlsx')
    sheet = wb['Data_Base']

    URL = sheet['A2'].value + user_search
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(sheet['C2'].value, class_=sheet['D2'].value)
    book_elements = results.find_all(sheet['E2'].value, class_=sheet['F2'].value)
    for book_element in book_elements:
        title = book_element.find(sheet['G2'].value)
        author = book_element.find(sheet['I2'].value, class_=sheet['J2'].value)
        price = book_element.find(sheet['K2'].value, class_=sheet['L2'].value)
        link = book_element.find(sheet['M2'].value)
        price = str(price.text.strip()).replace(' руб.', '')
        b = Book(title.text.strip(), author.text.strip(), price, str((sheet['O2'].value + str(link.get('href')))))
        Book.list_of_books.append(b)

    out()

"""print(title.text.strip())
print(author.text.strip())
print(str(price.text.strip()).replace(' руб.', ''))
print(sheet['O2'].value + str(link.get('href')))"""


#universal()
