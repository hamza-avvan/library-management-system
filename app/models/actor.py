from functools import wraps
from flask import g, request, redirect, session

class Actor():
	sess_key = ""
	route_url = "/"

	common_properties = ['name', 'email', 'id', 'created_at']
	specific_properties = []

	def __getattr__(self, name):
		if name in session:
			return session[name]
		
		raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


	def set(self, info):
		# Set common properties
		for key in self.common_properties:
			session[key] = info.get(key)
			setattr(session, key, info.get(key))

		# Set specific properties
		for key in self.specific_properties:
			session[key] = info.get(key)
			setattr(session, key, info.get(key))

		print(session)

	def uid(self):
		if self.isLoggedIn():
			return session[self.sess_key]

		return "err"

	def set_session(self, session, g):
		g.user = 0

		if self.isLoggedIn():
			g.user = session[self.sess_key]

	def isLoggedIn(self):
		if self.sess_key in session and session[self.sess_key] and session[self.sess_key]>0:
			return True

		return False

	def login_required(self, f, path="signin"):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if self.sess_key not in session or session[self.sess_key] is None:
				print(path)
				return redirect(self.route_url+path)
			return f(*args, **kwargs)
		return decorated_function

	def redirect_if_login(self, f, path="/"):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if self.sess_key in session and session[self.sess_key] is not None:
			    return redirect(self.route_url+path)
			return f(*args, **kwargs)
		return decorated_function

	def signout(self):
		session[self.sess_key] = None

	def signin(self):
		pass