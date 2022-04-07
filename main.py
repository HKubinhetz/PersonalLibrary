# todo - documentar e embelezar

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    bookid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    review = db.Column(db.Float, nullable=False)


def query_books():
    all_books = []
    books = db.session.query(Book).all()
    for book in books:
        book_info = {
            "bookid": book.bookid,
            "title": book.title,
            "author": book.author,
            "rating": book.review,
        }
        all_books.append(book_info)
    return all_books


def find_book(books, link_id):
    for book in books:
        print(books)
        print(link_id)
        if book['bookid'] == int(link_id):
            selected_book = book
            print(selected_book['title'])
            return selected_book

    print("Nao encontrei")
    return "Book not found"


@app.route('/')
def home():
    books = query_books()
    return render_template("index.html", books=books)


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
        return redirect(url_for('home'))

    if request.method == "GET":
        return render_template("add.html")


@app.route('/edit/<link_id>', methods=["GET", "POST"])
def edit(link_id):
    books = query_books()
    selected_book = find_book(books, link_id)

    if request.method == "POST":
        book_rating = request.form.get('rating')
        print(book_rating)
        book_to_update = Book.query.filter_by(bookid=link_id).first()
        book_to_update.review = book_rating
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", book=selected_book)


@app.route('/delete/<link_id>', methods=["GET", "POST"])
def delete(link_id):
    books = query_books()
    selected_book = find_book(books, link_id)

    if request.method == "POST":
        book_to_delete = Book.query.get(link_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('deletesuccess'))

    return render_template("delete.html", book=selected_book)


@app.route('/deletesuccess')
def deletesuccess():
    return render_template("deletesuccess.html")


if __name__ == "__main__":
    app.run(debug=True)

