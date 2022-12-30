from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# instead of saving the books into a list, we'll put them into a database
# create database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
db = SQLAlchemy(app=app)

# create the table
class Book(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String(250), unique=True, nullable=False)
    author  = db.Column(db.String(250), nullable=False)
    rating  = db.Column(db.Float, nullable=False)

app.app_context().push()
db.create_all()

# home page
@app.route('/')
def home():
    # CRUD - READ all books
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)    

# page to add books
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # instantiate new Book object
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
            )
        # add Book object to the database
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html')

# edit page for editing book ratings
@app.route('/edit', methods=['GET', 'POST'])
def edit_rating():

    if request.method == 'POST':
        # update record 
        book_id = request.form['id']
        update_book = Book.query.get(book_id)
        update_book.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))

    # get the current book id from Index.html, pass over Book object
    book_id = request.args.get('id')
    chosen_book = Book.query.get(book_id)
    # always try to pass object, rather than attributes
    return render_template('edit.html', book=chosen_book)

@app.route('/delete')
def delete():
    # delete book
    book_id = request.args.get('id')    # get the book id
    chosen_book = Book.query.get(book_id)   # get the book using the book id
    db.session.delete(chosen_book)      # delete the Book
    db.session.commit()
    return redirect(url_for('home'))    # redirect to the home page

if __name__ == "__main__":
    app.run(debug=True)

