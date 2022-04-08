# ---------------------------------- IMPORTS ----------------------------------
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# --------------------------- SERVER AND DB CREATION --------------------------
app = Flask(__name__)                                                               # Server Creation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'         # Database Connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                                # Don't track modifications
db = SQLAlchemy(app)                                                                # Database Creation


# ------------------------------ DATA STRUCTURE -------------------------------
class Book(db.Model):
    # This class defines all the columns for the data in the project
    # This is the exact same structure used on the Database Creation
    bookid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    review = db.Column(db.Float, nullable=False)


# --------------------------------- FUNCTIONS ---------------------------------
def query_books():
    # This function finds all books in the Database, if any, and returns them.
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
    # This function finds a specific book in the book list.
    for book in books:
        print(books)
        print(link_id)
        if book['bookid'] == int(link_id):
            selected_book = book
            print(selected_book['title'])
            return selected_book
    return "Book not found"


# ---------------------------------- ROUTING ----------------------------------
@app.route('/')
# Homepage routing. The page shows all existing books or if there aren't any,
# it returns an "empty library" message"
def home():
    books = query_books()
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
# Routing when the user decides to add a new book.
def add():

    if request.method == "GET":
        # If the page is first loading (GET), the server renders the form template.
        return render_template("add.html")

    if request.method == "POST":
        # When the form is submitted (POST), all data is transfered to the following lines.
        # They capture the inputs through the Flask "request" method.
        book_title = request.form.get('title')
        book_author = request.form.get('author')
        book_rating = request.form.get('rating')

        # Captured data is restructured to create a new record
        # User then gets redirected to homepage.
        new_book = Book(title=book_title, author=book_author, review=book_rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    else:
        # If method is neither, returns the originally intended page.
        return render_template("add.html")


@app.route('/edit/<link_id>', methods=["GET", "POST"])
# Routing when the user decides to edit book's rating.
def edit(link_id):
    books = query_books()
    selected_book = find_book(books, link_id)

    if request.method == "GET":
        # If the page is first loading (GET), the server renders the edit template.
        return render_template("edit.html", book=selected_book)

    if request.method == "POST":
        # When the form is submitted (POST), the code updates the existing book rating.
        # They capture the inputs through the Flask "request" method.
        book_rating = request.form.get('rating')                            # Grabs the new rating
        book_to_update = Book.query.filter_by(bookid=link_id).first()       # Finds the book in the DB
        book_to_update.review = book_rating                                 # Updates the rating
        db.session.commit()                                                 # Commits the update
        return redirect(url_for('home'))                                    # Redirects the user to home

    else:
        # If method is neither, returns the originally intended page.
        return render_template("edit.html", book=selected_book)


@app.route('/delete/<link_id>', methods=["GET", "POST"])
# Routing when the user decides to delete a book entry.
def delete(link_id):
    selected_book = find_book(query_books(), link_id)

    if request.method == "GET":
        # If the page is first loading (GET), the server renders the delete template.
        return render_template("delete.html", book=selected_book)

    if request.method == "POST":
        # When the form is submitted (POST), the code proceeds on the book exclusion.
        book_to_delete = Book.query.get(link_id)        # Finds the book to delete
        db.session.delete(book_to_delete)               # Deletes the book
        db.session.commit()                             # Commits the change
        return redirect(url_for('deletesuccess'))       # Redirects the user to home

    else:
        # If method is neither, returns the originally intended page.
        return render_template("delete.html", book=selected_book)


@app.route('/deletesuccess')
# Routing after a successful book exclusion.
def deletesuccess():
    return render_template("deletesuccess.html")


# --------------------------------- EXECUTION ---------------------------------
if __name__ == "__main__":
    app.run(debug=True)

