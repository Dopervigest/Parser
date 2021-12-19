from book import Book

# def out():
#     for book in Book.list_of_books:
#         print(book.title, book.author, book.price, book.link, sep="\n", end="\n \n")


def out():
    BookList = []
    i = 1
    for book in Book.list_of_books:
        d = {'number': i, 'title': book.title, 'author': book.author, 'price': book.price, 'link': book.link}
        i += 1
        BookList.append(d)
    return(BookList)
