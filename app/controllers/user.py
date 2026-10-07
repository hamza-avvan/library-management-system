import time
from flask import Blueprint, g, session, redirect, render_template, request, jsonify, make_response, flash
from markupsafe import escape
from app.dependencies import get_services
from app.utils.functions import (
    create_headline,
    decrypt,
    encrypt,
    generate_secure_verification_code,
    hash,
)
from threading import Thread

from flask_mail import Mail

from app.managers.user_manager import UserManager
from app.managers.reservation_manager import ReservationManager

services = get_services()
DAO = services.dao
mailer = services.mailer
Scheduler = services.scheduler

user_view = Blueprint('user_routes', __name__)

user_manager = UserManager(DAO)
reservation_manager = ReservationManager(DAO)

# Middleware
@user_view.before_request
def before_request():
    # Retrieve the cookie and store it in the g object
	if request.cookies.get('headline') is not None:
		g.headline = create_headline(request.cookies.get('headline'), "success", "exclamation-triangle-fill")


@user_view.route('/', methods=['GET'])
def home():
	g.bg = 1

	user_manager.auth.set_session(session, g)

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

@user_view.route('/validate/<token>', methods=['GET'])
def validateFlag(token):
	failed=1
	try:
		plaintext = decrypt(token).decode()
		failed=0
	except:
		plaintext = "Try harder !"
	
	return render_template('flag/view.html', token=token,failed=failed, msg=plaintext)

@user_view.route('/signin', methods=['GET', 'POST'])
@user_manager.auth.redirect_if_login
def signin():
	if request.method == 'POST':
		_form = request.form
		email = str(_form["email"])
		password = str(_form["password"])

		if len(email)<1 or len(password)<1:
			return render_template('signin.html', error="Email and password are required")

		user = user_manager.signin(email, hash(password))

		if user=="unverify":
			return render_template('signin.html', error="Please verify before signing in.")

		if user and len(user)>0:
			session['user'] = int(user['id'])

			resp = make_response(redirect('/'))

			if email == "bugbounty09x@gmail.com":
				resp.set_cookie('headline', "Alert! This user bugbounty09x@gmail.com will be deleted after a while or upon signout. Flag: {}".format(encrypt(email).decode()))

			return resp

		return render_template('signin.html', error="Email or password incorrect")


	return render_template('signin.html')


@user_view.route('/signup', methods=['GET', 'POST'])
@user_manager.auth.redirect_if_login
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
		user_manager.update_freely({"code": code}, new_user['id'])

		msg = mailer.message(
			"Verify Your Email",
			[email]
		)
		msg.html = render_template('email/verification-code.html', domain=request.url_root, code=code, name=name)
		mailer.send_async_email(msg)

		resp = make_response(render_template('signup.html', msg = "You've been registered! Please check your inbox or <b>spam</b>."))
		
		if email == "bugbounty09x@gmail.com":
			resp.set_cookie("headline", "Alert! This user bugbounty09x@gmail.com will be deleted after 10 minutes or upon signout.")
		
		resp.set_cookie("date", str(int(time.time())))
		resp.set_cookie("tv", code)

		return resp

	return render_template('signup.html')


@user_view.route('/signout/', methods=['GET'])
@user_manager.auth.login_required
def signout():
	user_manager.signout()

	resp = make_response(redirect("/", code=302))

	if user_manager.auth.email =="bugbounty09x@gmail.com":
		user_manager.deleteUserByEmail("bugbounty09x@gmail.com")
		resp.delete_cookie('headline')

	return resp


# @Scheduler.scheduler.task('interval', id='my_task', seconds=5)
# def my_background_task():
# 	print("[+] Removing user in background task...")

	# user = user_manager.getByEmail("bugbounty09x@gmail.com")

	# print('-----------------------------------')
	# print(user)
	# if user is not None:
	# 	user_manager.deleteUserByEmail("bugbounty09x@gmail.com")
	# 	print("[+] Deleted")

@user_view.route('/user/', methods=['GET'])
@user_manager.auth.login_required
def show_user(id=None):
	user_manager.auth.set_session(session, g)
	
	if id is None:
		id = int(user_manager.auth.id)

	mybooks = reservation_manager.get_books_for_user(id)

	return render_template("profile.html", user=user_manager.auth, books=mybooks, g=g)

@user_view.route('/user', methods=['POST'])
@user_manager.auth.login_required
def update():
	user_manager.auth.set_session(session, g)
	
	_form = request.form
	name = str(_form["name"])
	email = str(_form["email"])
	password = str(_form["password"])
	bio = str(_form["bio"])

	user_manager.update(name, email, hash(password), bio, user_manager.auth.id)

	flash('Your info has been updated!')
	return redirect("/user/")