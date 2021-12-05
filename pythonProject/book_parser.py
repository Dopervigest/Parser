import urllib

from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.title = []
        self.author = []
        self.price = []
        self.link = []
        self.user_search = ''
        self.search_len = 0

    def new_search(self):
        self.user_search = input("Какую книгу вы хотите найти?:   ")

    def single_output(self):
        for i in range(self.search_len, len(self.title)):
            print(self.title[i] + "  -  " + self.author[i])
            print(self.price[i])
            print(self.link[i])
        self.search_len = len(self.title)

    def bukvoed(self):
        URL = "https://www.bookvoed.ru/books?q=" + self.user_search
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="books")
        book_elements = results.find_all("div", class_="Lh")
        for book_element in book_elements:
            title = book_element.find("div", class_="Lr Mr")
            if title is None:        # по какой-то причине, после определенной книге на странице дальше указывается другой класс
                title = book_element.find("a", class_="KLb Or")
            if title is None:
                title = book_element.find("a", class_="MLb Or")
            if title is None:
                continue
            author = book_element.find("div", class_="Pr")
            price = book_element.find("div", class_="xg")
            if price is None:        # если книги нет в наличии, цена указывается в другом классе
                price = book_element.find("div", class_="yg")
            link = book_element.find("a", class_="Ir Jr")
            self.title.append(title.text.strip())
            self.author.append(author.text.strip())
            self.price.append(str(price.text.strip()).replace('\u202f₽', ''))
            self.link.append(link.get('href'))

    def knigosvet(self):
        URL = "https://www.knigosvet.com/search.php?param=1&keyword=" + self.user_search
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="productGrid")
        book_elements = results.find_all("ul", class_="bookcard")
        for book_element in book_elements:
            title_and_author = book_element.find("h1", class_="showName")
            price = book_element.find("span", class_="salePrice")
            link = book_element.find("a", target="_blank")
            items = str(title_and_author.text.strip()).split("\n")
            self.title.append(items[0])
            if items[-1] == items[0]:
                self.author.append('')
            else:
                self.author.append(items[-1])
            if price is None:
                self.price.append('')
            else:
                self.price.append(str(price.text.strip()).replace(' руб', ''))
            self.link.append('https://www.knigosvet.com' + str(link.get('href')))

    def bookean(self):
        URL = "http://bookean.ru/catalog-books/?q=" + self.user_search
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", class_="row grid-space-10")
        book_elements = results.find_all("div", class_="col-md-3 col-sm-4 masonry-grid-item")
        for book_element in book_elements:
            title = book_element.find("h3")
            author = book_element.find("p", class_="small")
            price = book_element.find("span", class_="price")
            link = book_element.find("a")
            self.title.append(title.text.strip())
            self.author.append(author.text.strip())
            self.price.append(str(price.text.strip()).replace(' руб.', ''))
            self.link.append("http://bookean.ru" + str(link.get('href')))

    def bookskazan(self):
        for i in range(1, 100):
            URL = "https://bookskazan.ru/catalog/?page=" + str(i) + "&q=" + self.user_search
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("ul", class_="book-list content-razdel")
            try:
                book_elements = results.find_all("li", class_="book-list__item__big-card")
            except AttributeError:
                break
            for book_element in book_elements:
                title = book_element.find("span", class_="card-hover__book-title")
                author = book_element.find("span", class_="card-hover__autor")
                price = book_element.find("p", class_="b-card__price discount-price")
                if price is None:
                    price = book_element.find("p", class_="b-card__price old-price")
                link = book_element.find("a", class_="product-link")
                self.title.append(title.text.strip())
                if author:
                    self.author.append(author.text.strip())
                else:
                    self.author.append('')
                if price:
                    self.price.append(str(price.text.strip()).replace('i', ''))
                else:
                    self.price.append('')
                self.link.append("http://bookskazan.ru" + str(link.get('href')))
            i = i + 1

    def fkniga(self):
        URL = "https://fkniga.ru/search/?q=" + self.user_search.replace(" ", "+")
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", class_="category-cards-container js-catalog-content")
        if results:
            book_elements = results.find_all("div", class_="grid__item columnDesktop--3 columnSmallDesktop--4 columnTablet--4 columnMobile--12")
            for book_element in book_elements:
                title = book_element.find("a", class_="card__title")
                author = book_element.find("div", class_="card__subtitle")
                price = book_element.find("div", class_="price price--ruble")
                link = book_element.find("a")
                self.title.append(title.text.strip())
                if author:
                    self.author.append(author.text.strip())
                else:
                    self.author.append("")
                self.price.append(str(price.text.strip()))
                self.link.append("https://fkniga.ru" + link.get('href'))

    def book24(self):
        count = 1
        for i in range(100):
            if i == 0:
                URL = "https://book24.ru/search/?q=" + self.user_search
            else:
                URL = "https://book24.ru/search/page-" + str(count) + "/?q=" + self.user_search
            count += 1
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("div", class_="catalog__product-list-holder")
            if results:
                book_elements = results.find_all("div", class_="product-card__content")
                for book_element in book_elements:
                    title = book_element.find("a", class_="product-card__name smartLink")
                    author = str(book_element.find("a", class_="author-list__item smartLink"))
                    price = book_element.find("div", class_="product-card-price__current")
                    link = book_element.find("a", class_="product-card__name smartLink")
                    if title:
                        if price is None:
                            continue
                        self.title.append(title.get("title"))
                        if author == "None" or author is None:
                            self.author.append("")
                        else:
                            self.author.append(author[author.find('">') + 2: author.find('</a>')])
                        self.price.append(str(price.text.strip()).replace('\xa0', '').replace(' р.', ''))
                        self.link.append("https://book24.ru" + link.get('href'))
                    else:
                        break
            else:
                break

    def labirint(self):
        count, results1 = 1, ""
        for i in range(100):
            if i == 0:
                URL = "https://www.labirint.ru/search/" + self.user_search + "/?stype=0"
            else:
                URL = "https://www.labirint.ru/search/" + self.user_search + "/?stype=0&page=" + str(count)
            count += 1
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("div", class_="products-row-outer responsive-cards")
            book_elements = results.find_all("div", class_="card-column card-column_gutter col-xs-6 col-sm-3 col-md-1-5 col-xl-2")
            if i == 0:
                results1 = results
            elif results1 == results:
                break
            if book_elements:
                for book_element in book_elements:
                    title = book_element.find("span", class_="product-title")
                    author = book_element.find("div", class_="product-author")
                    price = book_element.find("span", class_="price-val")
                    link = book_element.find("a", class_="product-title-link")
                    if title:
                        if price is None:
                            continue
                        self.title.append(title.text.strip())
                        if author is None:
                            self.author.append("")
                        else:
                            self.author.append(author.text.strip())
                        self.price.append(price.text.strip().replace(" ₽", ""))
                        self.link.append("https://www.labirint.ru" + link.get('href'))
                    else:
                        break
            else:
                break

    def prodalit(self):
        for i in range(1, 100):
            URL = "https://www.prodalit.ru/cat?FindMode=Short&SearchText=" + self.user_search.replace(" ", "+") + "&PageNumber=" + str(i)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("div", class_="tg-products tg-products-5")
            try:
                book_elements = results.find_all("div", class_="vtProduct")
            except AttributeError:
                break
            for book_element in book_elements:
                title = book_element.find("h3")
                author = book_element.find("div", class_="tg-bookwriter")
                price = book_element.find("ins")
                link = book_element.find("a")
                self.title.append(title.text.strip().replace("\n", " "))
                self.author.append(author.text.strip())
                self.price.append(price.text.strip())
                self.link.append("https://www.prodalit.ru" + link.get('href'))

    def books_moda(self):
        for i in range(5):
            URL = "https://books.moda/search?srch=" + self.user_search.replace(" ", "+") + "&page=" + str(i)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("section", id="block-system-main")
            try:
                book_elements = results.find_all("div", class_="views-row")
            except AttributeError:
                break
            for book_element in book_elements:
                title = book_element.find("div", class_="title")
                price = book_element.find("span", class_="value")
                link = title.find("a")
                self.title.append(title.text.strip())
                self.author.append('')
                self.price.append(price.text.strip().replace(" ", ""))
                self.link.append("https://books.moda" + link.get('href'))

    def dreamers(self):  # фантазёры.рф
        for i in range(1, 10):
            URL = "https://фантазеры.рф/search/?page=" + str(i) + "&query=" + self.user_search.replace(" ", "+")
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("div", id="product-list")
            try:
                book_elements = results.find_all("div", class_="product flexdiscount-product-wrap")
            except AttributeError:
                break
            for book_element in book_elements:
                title = book_element.find("a")
                price = book_element.find("span", class_="price price-new nowrap")
                if price is None:
                    price = book_element.find("span", class_="price nowrap")
                self.title.append(title.get('title'))
                self.author.append('')
                self.price.append(price.text.strip().replace(" ₽", "").replace(" ", ""))
                self.link.append("https://фантазеры.рф" + title.get('href'))

    def domknigi(self):
        for i in range(1, 10):
            URL = "https://domknigi-online.ru/search?search=" + self.user_search + "&search_type=full&page=" + str(i)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("ul", class_="product_carousel product_carousel_4 clearfix")
            try:
                book_elements = results.find_all("li", class_="product-layout list-unstyled list-inline")
            except AttributeError:
                break
            for book_element in book_elements:
                title = str(book_element.find("span", class_="product_title").find("a"))
                price = book_element.find("span", class_="product_count pull-left")
                if price is None:
                    continue
                link = book_element.find("span", class_="product_title").find("a").get("href")
                self.title.append(title[title.find('">') + 2: title.find('</a>')])
                self.author.append('')
                self.price.append(price.text.strip())
                self.link.append(link)

    def korobkaknig(self):
        for i in range(1, 10):
            if i == 1:
                URL = "https://korobkaknig.ru/search/?search=" + self.user_search + "&description=true"
            else:
                URL = "https://korobkaknig.ru/search/?search=" + self.user_search + "&description=true" + "&page=" + str(i)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find("div", id="main_content")
            try:
                book_elements = results.find_all("div", class_="product-layout product-grid col-lg-4 col-md-6 col-sm-6 col-xs-12")
            except AttributeError:
                break
            for book_element in book_elements:
                title = str((book_element.find("div", class_="caption")).find("a"))
                if title is None:
                    continue
                price = book_element.find("p", class_="price")
                if price is None:
                    continue
                link = book_element.find("div", class_="caption").find("a").get("href")
                author = book_element.find("div", class_="attribute").find("span", class_="attr_value")
                self.title.append(title[title.find('">') + 2: title.find('</a>')])
                self.author.append(author.text.strip())
                self.price.append(price.text.strip().replace(" р.", ""))
                self.link.append(link)

    def bukinist(self):
        URL = "https://bukinistkniga.ru/all-products/page-all?keyword=" + self.user_search
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", id="fn_products_content")
        try:
            book_elements = results.find_all("div", class_="col-sm-6 col-xl-4")
        except AttributeError:
            return
        for book_element in book_elements:
            title = str((book_element.find("div", class_="preview_details")).find("a"))
            if title is None:
                continue
            price = book_element.find("div", class_="price")
            if price is None:
                continue
            link = book_element.find("a", class_="product_name").get("href")
            self.title.append(title[title.find('">') + 2: title.find('</a>')])
            self.author.append("")
            self.price.append(price.text.strip().replace(" руб", ""))
            self.link.append("https://bukinistkniga.ru/" + link)

    def azbuka96(self):
        URL = "http://azbuka96.ru/search/query/" + self.user_search
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", id="catalog")
        try:
            book_elements = results.find_all("div", class_="block_item")
        except AttributeError:
            return
        for book_element in book_elements:
            title = book_element.find("div", class_="item").find("a")
            if title:
                title = title.text.strip()
                title = title[: title.find("/")]
                print(title)
            else:
                continue
            price = book_element.find("div", class_="item_price")
            link = book_element.find("div", class_="item_name").find("a").get("href")
            self.title.append(title)
            self.author.append("")
            self.price.append(price.text.strip().replace(" р", ""))
            self.link.append(link)

    def respublica(self):
        URL = "https://www.respublica.ru/search?query=" + self.user_search + "&category_id=1"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", class_="page")
        try:
            book_elements = results.find_all("div", class_="item")
        except AttributeError:
            return
        for book_element in book_elements:
            title = (book_element.find("div", class_="title")).find("a").get("title")
            if title is None:
                continue
            price = book_element.find("div", class_="price")
            if price is None:
                continue
            link = book_element.find("a", class_="title-link").get("href")
            author = book_element.find("a", class_="brand-link").get("title")
            self.title.append(title)
            if author:
                self.author.append(author)
            else:
                self.author.append("")
            self.price.append(price.text.strip().replace(" руб.", "").strip())
            self.link.append("https://www.respublica.ru/" + link)

    def books(self):     #надо проверить на страницы
        s = HTMLSession()
        for i in range(1, 6):
            if i == 1:
                URL = "https://www.books.ru/search.php?s%5Bquery%5D=" + self.user_search.replace(" ","+") + "&s%5Bpresence%5D=all&s%5Bscope%5D=everywhere&s%5Bgo%5D=1&passing=1&s[type_of_addon]=books"
            else:
                URL = "https://www.books.ru/search.php?s%5Bquery%5D=" + self.user_search.replace(" ","+") + "s%5Bpresence%5D=all&s%5Bscope%5D=everywhere&s%5Bgo%5D=1&passing=1&s[type_of_addon]=books&page=" + str(i)
            session = s.get(URL)
            session.html.render(sleep=1, keep_page=True, scrolldown=1)
            soup = BeautifulSoup(session.content, "html.parser")
            results = soup.find("div", class_="catalog-main_row catalog-main_row_card")
            try:
                book_elements = results.find_all("div", class_="book-catalog_item")
            except AttributeError:
                return
            for book_element in book_elements:
                title = book_element.find("a", class_="custom-link book-catalog_item_title").get("data-title")
                if title is None:
                    continue
                price = book_element.find("span", class_="book-price")
                if price is None:
                    continue
                author = str(book_element.find("div", class_="book-catalog_item_author").find("a"))
                author = author[author.find('">') +2: author.find('</a>')]
                link = book_element.find("a", class_="custom-link book-catalog_item_title").get("href")
                self.title.append(title)
                self.price.append(price.text.strip().replace(" ₽", ""))
                if author == "on":
                    self.author.append("")
                else:
                    self.author.append(author)
                self.link.append("https://www.books.ru" + link)

    def libroroom(self):
        s = HTMLSession()
        URL = "https://libroroom.ru/catalog/?q=" + self.user_search.replace(" ", "+") + "&how=r"
        session = s.get(URL)
        session.html.render(sleep=1, keep_page=True, scrolldown=1)
        soup = BeautifulSoup(session.content, "html.parser")
        results = soup.find("div", class_="catalog block ajax_load search")
        try:
            book_elements = results.find_all("div", class_="catalog_item_wrapp")
        except AttributeError:
            return
        for book_element in book_elements:
            title = book_element.find("div", class_="item-title")
            if title is None:
                continue
            try:
                price = book_element.find("div", class_="price").get("data-value")
            except AttributeError:
                continue
            if price is None:
                continue
            link = book_element.find("div", class_="item-title").find("a").get("href")
            self.title.append(title.text.strip())
            self.price.append(price)
            self.author.append("")
            self.link.append("https://libroroom.ru/" + link)

    def clever(self):
        s = HTMLSession()
        URL = "https://www.clever-media.ru/search/?q=" + self.user_search.replace(" ", "+")
        session = s.get(URL)
        try:
            session.html.render(sleep=2, keep_page=True, scrolldown=1)
        except:
            return
        soup = BeautifulSoup(session.content, "html.parser")
        results = soup.find("div", class_="products-grid")
        try:
            book_elements = results.find_all("div", class_="item")
        except AttributeError:
            return
        for book_element in book_elements:
            title = book_element.find("div", class_="book-name").find("a", class_="js-item").get("data-name")
            if title is None:
                continue
            try:
                price = book_element.find("div", class_="book-price").find("div", class_="price v1").find("div", class_="price-new")
            except AttributeError:
                continue
            link = book_element.find("div", class_="book-name").find("a", class_="js-item").get("href")
            self.title.append(title)
            self.price.append(price.text.strip().replace("рублей", ""))
            self.author.append("")
            self.link.append("https://www.clever-media.ru" + link)

    def region(self):
        s = HTMLSession()
        URL = "https://regionbook.ru/search/?query=" + self.user_search.replace(" ", "+")
        session = s.get(URL)
        session.html.render(sleep=1, keep_page=True, scrolldown=2)
        soup = BeautifulSoup(session.content, "html.parser")
        results = soup.find("ul", class_="product-list expandable colored list")
        try:
            book_elements = results.find_all("div", class_="pl-item-wrapper")
        except AttributeError:
            return
        for book_element in book_elements:
            title = book_element.find("div", class_="pl-item-info-expandable").find("a").get("title")
            if title is None:
                continue
            try:
                price = book_element.find("div", class_="price-wrapper").find("span", class_="price nowrap")
            except AttributeError:
                continue
            if price is None:
                continue
            link = book_element.find("div", class_="pl-item-info-expandable").find("a").get("href")
            self.title.append(title)
            self.price.append(price.text.strip().replace(" ₽", ""))
            self.author.append("")
            self.link.append("https://regionbook.ru" + link)

    def alpina(self):
        s = HTMLSession()
        URL = "https://alpinabook.ru/catalog/search/?q=" + self.user_search.replace(" ", "+")
        session = s.get(URL)
        try:
            session.html.render(sleep=1, keep_page=True, scrolldown=2, timeout=10)
        except:
            return
        soup = BeautifulSoup(session.content, "html.parser")
        results = soup.find("div", class_="b-catalog-items")
        try:
            book_elements = results.find_all("div", class_="b-catalog-items__item")
        except AttributeError:
            return
        for book_element in book_elements:
            title = book_element.find("div", class_="b-book-v w-book-hover book-card bgColor-element gtm-book-card js-book-card _gray").get("data-book-name")
            if title is None:
                continue
            try:
                price = book_element.find("div", class_="b-book-v w-book-hover book-card bgColor-element gtm-book-card js-book-card _gray").get("data-book-price")
            except AttributeError:
                continue
            if int(price) == 0:
                continue
            link = book_element.find("div", class_="b-book-v__title").find("a").get("href")
            author = book_element.find("div", class_="b-book-v__author").find("span")
            try:
                author = author.text.strip()
            except:
                author = ""
            self.title.append(title)
            self.price.append(price)
            self.author.append(author)
            self.link.append("https://alpinabook.ru" + link)

One = Parser()
One.new_search()
One.alpina()

print(One.title)
print(One.author)
print(One.price)
print(One.link)
print(len(One.title))
print(len(One.author))
print(len(One.price))
print(len(One.link))
#One.single_output()
#print(len(One.title))
#One.respublica()
#One.single_output()
#print(len(One.title))



# косячные: https://www.chitai-gorod.ru/, https://chitaina.ru/, https://my-shop.ru, https://knigi-market.ru
# Очень косячные: https://bookpiter.ru/, https://www.knor.ru

# косячные у меня:  https://strana-fantasy.ru/, https://slovo-shop.ru/, https://urizdat.ru/
