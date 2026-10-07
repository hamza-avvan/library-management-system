from flask import Blueprint, g, session, redirect, render_template, request, jsonify, Response
from markupsafe import escape
from app.dependencies import get_services
from app.utils.functions import create_headline

from app.managers.user_manager import UserManager
from app.managers.book_manager import BookManager
from app.managers.reservation_manager import ReservationManager

DAO = get_services().dao

book_view = Blueprint('book_routes', __name__)

book_manager = BookManager(DAO)
reservation_manager = ReservationManager(DAO)
user_manager = UserManager(DAO)


# Middleware
@book_view.before_request
def before_request():
    # Retrieve the cookie and store it in the g object
	if request.cookies.get('headline') is not None:
		g.headline = create_headline(request.cookies.get('headline'), "warning", "exclamation-triangle-fill")


@book_view.route('/books/', defaults={'id': None})
@book_view.route('/books/<int:id>')
def home(id):
	user_manager.auth.set_session(session, g)

	user_books = []
	if user_manager.auth.isLoggedIn():
		reserved_books = reservation_manager.get_reserved_books_by_user(user_manager.auth.uid())
		user_books = (reserved_books.get('user_books', '') or '').split(',') if reserved_books.get('user_books', '') else []

	if id is not None:
		b = book_manager.getBook(id)
		template = 'book_view.html'
	else:
		b = book_manager.list()
		template = 'books.html'

	if not b:
		return render_template(template, error="No book(s) found!")

	return render_template(template, books=b, g=g, count=len(b), user_books=user_books)

@book_view.route('/books/me')
@user_manager.auth.login_required
def mybooks():
	user_manager.auth.set_session(session, g)

	user_books = []
	reserved_books = reservation_manager.get_reserved_books_by_user(user_manager.auth.uid())
	user_books = (reserved_books.get('user_books', '') or '').split(',') if reserved_books.get('user_books', '') is not None else []
	b = reservation_manager.get_books_for_user(user_manager.auth.uid())

	if not b:
		return render_template('books.html', error="No book(s) found!", view='mybooks')
	
	return render_template('books.html', books=b, g=g, user_books=user_books, count=len(user_books), view='mybooks')

@book_view.route('/books/add/<id>', methods=['GET'])
@user_manager.auth.login_required
def add(id):
	user_id = user_manager.auth.uid()

	reserved_books = reservation_manager.get_reserved_books_by_user(user_manager.auth.uid())
	reserved_books = (reserved_books.get('user_books', '') or '').split(',') if reserved_books else []
	
	b = book_manager.list()
	if id in reserved_books:
		return render_template("books.html", error="Book already reserved", books=b, g=g, user_books=reserved_books)
		
	reservation_manager.reserve_for_user(user_id, id)
	user_manager.auth.set_session(session, g)
	
	return render_template("books.html", msg="Book reserved", books=b, g=g, user_books=reserved_books)


@book_view.route('/books/search', methods=['GET'])
def search():
	user_manager.auth.set_session(session, g)
	
	reserved_books = reservation_manager.get_reserved_books_by_user(user_manager.auth.uid())
	reserved_books = (reserved_books.get('user_books', '') or '').split(',') if reserved_books else []

	if "keyword" not in request.args:
		return render_template("search.html")

	keyword = request.args["keyword"]

	if len(keyword)<1:
		return redirect('/books')

	d=book_manager.search(keyword)

	if len(d) >0:
		return render_template("books.html", search=True, books=d, count=len(d), keyword=escape(keyword), g=g, user_books=reserved_books)

	return render_template('books.html', error="No books found!", keyword=escape(keyword), user_books=reserved_books)
