from functools import wraps

from flask import redirect, session


class BaseAuthContext:
	session_key = None
	route_url = "/"
	session_fields = ()

	def __init__(self):
		if self.session_key is None:
			raise TypeError("BaseAuthContext must be initialized through a role-specific subclass")

	def __getattr__(self, name):
		if name in session:
			return session[name]
		raise AttributeError("{} has no attribute {!r}".format(type(self).__name__, name))

	def set(self, info):
		for key in self.session_fields:
			if key in info:
				session[key] = info[key]

	def uid(self):
		if self.isLoggedIn():
			return session[self.session_key]
		return "err"

	def set_session(self, current_session, g):
		g.user = current_session.get(self.session_key) or 0

	def isLoggedIn(self):
		user_id = session.get(self.session_key)
		return bool(user_id and user_id > 0)

	def login_required(self, function, path="signin"):
		@wraps(function)
		def decorated_function(*args, **kwargs):
			if self.session_key not in session or session[self.session_key] is None:
				return redirect(self.route_url + path)
			return function(*args, **kwargs)
		return decorated_function

	def redirect_if_login(self, function, path="/"):
		@wraps(function)
		def decorated_function(*args, **kwargs):
			if self.session_key in session and session[self.session_key] is not None:
				return redirect(self.route_url + path)
			return function(*args, **kwargs)
		return decorated_function

	def signout(self):
		session[self.session_key] = None