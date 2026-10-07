from flask import Blueprint, g, session, redirect, render_template, request, jsonify, Response
from markupsafe import escape
from app.dependencies import get_services
from app.utils.functions import ago, hash

from app.managers.admin_manager import AdminManager
from app.managers.book_manager import BookManager
from app.managers.reservation_manager import ReservationManager
from app.managers.user_manager import UserManager

DAO = get_services().dao

admin_view = Blueprint(
	'admin_routes',
	__name__,
	template_folder='../../templates/admin',
	url_prefix='/admin',
)

book_manager = BookManager(DAO)
reservation_manager = ReservationManager(DAO)
user_manager = UserManager(DAO)
admin_manager = AdminManager(DAO)


@admin_view.route('/', methods=['GET'])
@admin_manager.auth.login_required
def home():
	admin_manager.auth.set_session(session, g)

	return render_template('admin/home.html', g=g)


@admin_view.route('/signin/', methods=['GET', 'POST'])
@admin_manager.auth.redirect_if_login
def signin():
	g.bg = 1
	
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('admin/signin.html', error="Email and password are required")

		d = admin_manager.signin(email, hash(password))

		if d and len(d)>0:
			session['admin'] = int(d["id"])

			return redirect("/admin")

		return render_template('admin/signin.html', error="Email or password incorrect")

	return render_template('admin/signin.html')


@admin_view.route('/signout/', methods=['GET'])
@admin_manager.auth.login_required
def signout():
	admin_manager.signout()

	return redirect("/admin/", code=302)


@admin_view.route('/users/view/', methods=['GET'])
@admin_manager.auth.login_required
def users_view():
	admin_manager.auth.set_session(session, g)

	id = int(admin_manager.auth.uid())
	admin = admin_manager.get(id)
	# myusers = admin_manager.getUsersList()

	return render_template('user/index.html', g=g, admin=admin)

@admin_view.route('/users/search', methods=['GET'])
@admin_manager.auth.login_required
def search_users():
	admin_manager.auth.set_session(session, g)

	query = request.args.get('q', '').strip()
	page = max(request.args.get('page', 1, type=int), 1)
	per_page = min(max(request.args.get('per_page', 8, type=int), 1), 100)
	users, total = user_manager.search(query, per_page, (page - 1) * per_page)
	pages = max((total + per_page - 1) // per_page, 1)
	page = min(page, pages)

	if page != request.args.get('page', 1, type=int):
		users, total = user_manager.search(query, per_page, (page - 1) * per_page)

	return jsonify({
		"users": [
			{
				"id": user["id"],
				"name": user["name"],
				"email": user["email"],
				"bio": user["bio"],
				"mob": str(user["mob"] or "0"),
				"lock": int(user["lock"] or 0),
				"verify": int(user["verify"] or 0),
				"created_at": user["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
				"ago": ago(user["created_at"]),
			}
			for user in users
		],
		"total": total,
		"page": page,
		"pages": pages,
	})

@admin_view.route('/users/view/<int:uid>', methods=['GET'])
@admin_manager.auth.login_required
def view_user(uid):
	admin_manager.auth.set_session(session, g)

	id = int(admin_manager.auth.uid())
	admin = admin_manager.get(id)
	user = user_manager.get(uid)
	user_books = reservation_manager.get_books_for_user(uid)

	return render_template('user/view.html', g=g, books=user_books, user=user, admin=admin)


@admin_view.route('/books/', methods=['GET'])
@admin_manager.auth.login_required
def books():
	admin_manager.auth.set_session(session, g)

	id = int(admin_manager.auth.uid())
	admin = admin_manager.get(id)
	mybooks = book_manager.list(availability=0)

	return render_template('books/views.html', g=g, books=mybooks, admin=admin)

@admin_view.route('/books/<int:id>')
@admin_manager.auth.login_required
def view_book(id):
	admin_manager.auth.set_session(session, g)

	if id != None:
		b = book_manager.getBook(id)
		users = reservation_manager.get_borrowers_for_book(id)

		if b and len(b) <1:
			return render_template('books/book_view.html', error="No book found!")

		return render_template("books/book_view.html", books=b, books_owners=users, g=g)


@admin_view.route('/books/add', methods=['GET', 'POST'])
@admin_manager.auth.login_required
def book_add():
	admin_manager.auth.set_session(session, g)
	
	return render_template('books/add.html', g=g)


@admin_view.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@admin_manager.auth.login_required
def book_edit(id):
	admin_manager.auth.set_session(session, g)

	if id != None:
		b = book_manager.getBook(id)

		if b and len(b) <1:
			return render_template('edit.html', error="No book found!")

		return render_template("books/edit.html", book=b, g=g)
	
	return redirect('/books')

@admin_view.route('/books/delete/<int:id>', methods=['GET'])
@admin_manager.auth.login_required
def book_delete(id):
	id = int(id)

	if id is not None:
		book_manager.delete(id)
	
	return redirect('/admin/books/')


@admin_view.route('/books/search', methods=['GET'])
@admin_manager.auth.login_required
def search():
	admin_manager.auth.set_session(session, g)

	if "keyword" not in request.args:
		return render_template("books/view.html")

	keyword = request.args["keyword"]

	if len(keyword)<1:
		return redirect('/admin/books')

	id = int(admin_manager.auth.uid())
	admin = admin_manager.get(id)

	d=book_manager.search(keyword, 0)

	if len(d) >0:
		return render_template("books/views.html", search=True, books=d, count=len(d), keyword=escape(keyword), g=g, admin=admin)

	return render_template('books/views.html', error="No books found!", keyword=escape(keyword))
