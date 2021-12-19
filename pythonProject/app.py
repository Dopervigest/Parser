from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/search/<variable>')
def search(variable):
    BookList = [{'number': 0, 'title': 'Книга1', 'author': 'Автор1', 'price': '100', 'link': 'Ссылка1'},
                {'number': 1, 'title': 'Книга2', 'author': 'Автор2', 'price': '200', 'link': 'Ссылка2'},
                {'number': 2, 'title': 'Книга3', 'author': 'Автор3', 'price': '300', 'link': 'Ссылка3'}]
    return render_template("search.html", user_string=variable, list=BookList)


if __name__ == "__main__":
    app.run(debug="True")
