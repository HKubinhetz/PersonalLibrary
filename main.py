from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
all_books = []


class Book(db.Model):
    bookid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    review = db.Column(db.Float, nullable=False)


def query_books():
    books = db.session.query(Book).all()
    for book in books:
        book_info = {
            "id": book.bookid,
            "title": book.title,
            "author": book.author,
            "rating": book.review,
        }
        all_books.append(book_info)


@app.route('/')
def home():
    query_books()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_title = request.form.get('title')
        book_author = request.form.get('author')
        book_rating = request.form.get('rating')

        # Create a new record
        new_book = Book(title=book_title, author=book_author, review=book_rating)
        db.session.add(new_book)
        db.session.commit()
        query_books()
        return redirect(url_for('home'))

    if request.method == "GET":
        return render_template("add.html")


# todo - capturar esses caras e criar botões no HTML pra mostrar somente o livro que eu quiser editar/deletar
@app.route('/edit/<bookid>')
def edit(bookid):
    pass
    # return render_template("index.html", books=all_books)


@app.route('/delete/<bookid>')
def delete(bookid):
    pass
    # return render_template("index.html", books=all_books)


if __name__ == "__main__":
    app.run(debug=True)

