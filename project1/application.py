import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
	if session.get('user') == None:
		return render_template('index.html', invalid=False)
	else:
		return redirect(url_for('dashboard'))


@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html", user=session['user'])

@app.route("/register")
def register():
	return render_template('register.html', used=False)

@app.route("/registration", methods=['POST'])
def registration():
	username = request.form.get("username")
	if db.execute("SELECT username FROM tb_users WHERE username = :username",{"username": username}).rowcount != 0:
		return render_template('register.html', used=True)
	password = request.form.get('password')
	db.execute('INSERT INTO tb_users (username, password) VALUES (:username, :password)',
		{"username": username, "password": password})
	db.commit()
	return render_template("success_registration.html")

@app.route("/login", methods=['POST'])
def login():
	username = request.form.get('username')
	password = request.form.get('password')
	if db.execute("SELECT id FROM tb_users WHERE username = :username AND password = :password",
		{"username": username, "password": password}).rowcount == 0:
		return render_template("index.html", invalid=True)
	session['user'] = db.execute('SELECT id, username FROM tb_users WHERE username = :username AND password = :password',
		{"username": username, "password": password}).fetchone()
	return render_template("dashboard.html", user=session['user'])

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route("/book", methods=['GET'])
def book():
	comments = []
	lista = []
	commented = False
	a = session['user']
	id = request.args.get('id')
	book = db.execute("SELECT id, isbn, title, author, year FROM tb_books WHERE id = :id",
		{"id": id}).fetchone()
	if db.execute('SELECT id FROM tb_reviews WHERE id_user = :id_user AND id_book = :id_book',
		{'id_user': a.id, 'id_book': book.id}).rowcount != 0:
		commented = True
	comments = db.execute("SELECT username, comment, rate FROM tb_reviews JOIN tb_users ON tb_reviews.id_user = tb_users.id WHERE tb_reviews.id_book = :id_book",
		{"id_book": id})
	try:
		res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "AeSZgRuuQa1FEGSr2AIfmA", "isbns": book.isbn})
		res = res.json()
		lista.append(res["books"][0]["average_rating"])
		lista.append(res["books"][0]["ratings_count"])
	except:
		lista.append('No rating')
		lista.append('No rating')

	return render_template("book.html", book=book, res=lista, user=session['user'], commented=commented, comments=comments)

@app.route("/search_book", methods=['POST'])
def search_book():
	isbn = request.form.get('isbn')
	title = request.form.get('title')
	author = request.form.get('author')
	if isbn != '':
		isbn = f'%{isbn}%'
	if title != '':
		title = f'%{title}%'
	if author != '':
		author = f'%{author}%'
	books = db.execute("SELECT id, isbn, title, author FROM tb_books WHERE isbn LIKE :isbn OR LOWER(title) LIKE LOWER(:title) OR LOWER(author) LIKE LOWER(:author)",
		{"author": author, "title": title, "isbn": isbn}).fetchall()
	return render_template("dashboard.html", books=books, user=session['user'])

@app.route("/register_review", methods=['GET','POST'])
def register_review():
	lista = []
	rate = request.form.get('rate')
	comment = request.form.get('myreview')
	id_book = request.args.get('id')
	user = session['user']
	db.execute('INSERT INTO tb_reviews (id_user, id_book, comment, rate) VALUES (:id_user, :id_book, :comment, :rate)',
		{'id_user': user.id, 'id_book': id_book, 'comment': comment, 'rate': rate})
	db.commit()
	return redirect(url_for('book', id=id_book))

@app.route("/api/<string:isbn>")
def book_api(isbn):
	book = db.execute("SELECT isbn, id, title, author, year FROM tb_books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
	if book is None:
		return jsonify({
			"message": "Not Found",
			"status": "404"
			})

	review_count = db.execute("SELECT COUNT(*) FROM tb_reviews WHERE id_book = :id_book", {"id_book": book.id}).fetchone()
	average_acore = db.execute("SELECT AVG(rate) FROM tb_reviews WHERE id_book = :id_book", {"id_book": book.id}).fetchone()

	if average_acore.avg == None:
		return jsonify({
			"isbn": book.isbn,
			"title": book.title,
			"author": book.author,
			"year": book.year,
			"review_count": str(review_count[0]),
			"average_acore": 'No score'
		})

	return jsonify({
			"isbn": book.isbn,
			"title": book.title,
			"author": book.author,
			"year": book.year,
			"review_count": str(review_count[0]),
			"average_acore": str(format(average_acore.avg, '.1f'))
		})
	