from book import Book

def out():
    for book in Book.list_of_books:
        print(book.title, book.author, book.price, book.link, sep="\n", end="\n \n")
