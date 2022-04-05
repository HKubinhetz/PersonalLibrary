from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# todo - use commented code below to implement all the required functionalities

# # Update a given entry:
# book_to_update = Book.query.filter_by(title="Harry Potter").first()
# book_to_update.title = "Harry Potter and the Chamber of Secrets"
# db.session.commit()

# # Delete a given entry:
# book_id = 3
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()

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


# todo - capturar esses caras e criar botões no HTML pra mostrar somente o livro que eu quiser editar/deletar
@app.route('/edit/<bookid>')
def edit(bookid):
    books = query_books()
    return render_template("edit.html", books=books)


@app.route('/delete/<bookid>')
def delete(bookid):
    books = query_books()
    return render_template("delete.html", books=books)


if __name__ == "__main__":
    app.run(debug=True)

