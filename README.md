# Parser project
Данный проект является работой четырех студентов первого курса магистратуры ИнФО группы ФОМ-111001.
Состав команды: 

Дордюк Владислав Дмитриевич - программист 

Загребин Павел Эдуардович - программист

Пыхтеева Наталья Петровна - дизайнер, тестировщик 

Баева Наталия Владимировна - аналитик, тестировщик

Суть проекта заключается в создании парсера 20 популярных российских сайтов книг. 

Программа получает на вход название книги или имя автора, проводит поиск совпадений на книжных сайтах на основании запросов к форме поиска интернет-магазина и подает на вывод название книги, автора, цену и ссылку. 

Программа реализуется на языке программирования python, для хранения списка сайтов и их тэгов используется json

Архитектура программы:

main.py - мейн файл, запускает работу программы

Parser.py - функция парсинга запускается вызовом из main.py, считывает Database.json, собирает информацию с сайтов по тэгам и очищает её, создает экземпляр класса Book, записывает в массив list_of_books и отправляет в Out.py, где он обрабатывается, после этого передает его в main 

book.py - класс книги, экземпляры данного класса имеют следующие аттрибуты: название книги(title), автор книги(author), цена книги(price) и ссылка на данную книгу в магазине(link). Также содержит массив list_of_books в котором хранятся созданные экземпляры класса 

Out.py - получает массив list_of_books, собирает словарь и возвращает его

app.py - 

Database.json - json файл в котором хранится список site_info, каждый его элемент - это сайт с тегами для парсинга, которые необходимы для работы функции из Parser.py

templates - хранит html файлы
