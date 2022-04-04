from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
all_books = []


@app.route('/')
def home():
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_title = request.form.get('title')
        book_author = request.form.get('author')
        book_rating = request.form.get('rating')

        book_info = {
            "title": book_title,
            "author": book_author,
            "rating": book_rating,
        }

        print(book_info)
        all_books.append(book_info)

        return render_template("index.html", books=all_books)

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

