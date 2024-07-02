from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash
from app import DAO, mailer
from Misc.functions import *
from threading import Thread

from flask_mail import Mail

from Controllers.UserManager import UserManager

user_view = Blueprint('user_routes', __name__, template_folder='/templates')

user_manager = UserManager(DAO)

@user_view.route('/', methods=['GET'])
def home():
	g.bg = 1

	user_manager.user.set_session(session, g)
	print(g.user)

	return render_template('home.html', g=g)

@user_view.route('/email', methods=['GET'])
def testemail():
	msg = mailer.message(
        "Verify Your Email",
        ["reciever@example.com"]
    )

	msg.html = render_template('email/verification-code.html', domain=request.url_root, code=123)
	mailer.send_async_email(msg)
	# mailer.mail.send(msg)
	
# 	user_manager.update_freely({"code": str("asas")}, 1)
# 	code = generate_secure_verification_code('asas')
# 	return code
	return render_template('email/verification-code.html', domain=request.url_root, code=123)

@user_view.route('/verify/<code>', methods=['GET'])
def verifyUser(code):
	user = user_manager.getUserByCode(code)

	if user:
		user_manager.update_freely({"verify": 1}, user['id'])
	
		flash('User verification successful!')
		return redirect("/user/")

	return render_template('signin.html', error="Invalid verification code")

@user_view.route('/signin', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signin():
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('signin.html', error="Email and password are required")

		d = user_manager.signin(email, hash(password))

		if d=="unverify":
			return render_template('signin.html', error="Please verify before signing in.")

		if d and len(d)>0:
			session['user'] = int(d['id'])

			return redirect("/")

		return render_template('signin.html', error="Email or password incorrect")


	return render_template('signin.html')


@user_view.route('/signup', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signup():
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		password = request.form.get('password')

		if len(name) < 1 or len(email)<1 or len(password)<1:
			return render_template('signup.html', error="All fields are required")

		new_user = user_manager.signup(name, email, hash(password))

		if new_user == "already_exists":
			return render_template('signup.html', error="User already exists with this email")

		code = generate_secure_verification_code(email)
		print(code)
		user_manager.update_freely({"code": code}, new_user['id'])

		msg = mailer.message(
			"Verify Your Email",
			[email]
		)
		msg.html = render_template('email/verification-code.html', domain=request.url_root, code=code, name=name)
		mailer.send_async_email(msg)

		return render_template('signup.html', msg = "You've been registered! Please check your inbox or <b>spam</b>.")

	return render_template('signup.html')


@user_view.route('/signout/', methods=['GET'])
@user_manager.user.login_required
def signout():
	user_manager.signout()

	return redirect("/", code=302)

@user_view.route('/user/', methods=['GET'])
@user_manager.user.login_required
def show_user(id=None):
	user_manager.user.set_session(session, g)
	
	if id is None:
		id = int(user_manager.user.uid())

	d = user_manager.get(id)
	mybooks = user_manager.getBooksList(id)

	return render_template("profile.html", user=d, books=mybooks, g=g)

@user_view.route('/user', methods=['POST'])
@user_manager.user.login_required
def update():
	user_manager.user.set_session(session, g)
	
	_form = request.form
	name = str(_form["name"])
	email = str(_form["email"])
	password = str(_form["password"])
	bio = str(_form["bio"])

	user_manager.update(name, email, hash(password), bio, user_manager.user.uid())

	flash('Your info has been updated!')
	return redirect("/user/")