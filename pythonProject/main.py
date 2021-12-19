import Parser
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/search/<variable>')
def search(variable):
    BookList = Parser.universal(variable)
    return render_template("search.html", user_string=variable, list=BookList)


if __name__ == "__main__":
    app.run(debug="True")
