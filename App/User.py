from App.Actor import Actor

class User(Actor):
	id = 0
	name = ""
	email = ""
	lock = False
	code = ""

	user = {}

	def __init__(self, UserDAO):
		self.dao = UserDAO
		self.sess_key = "user" # session key

	def set(self, info):
		self.name = info['name']
		self.email = info['email']
		self.lock = info['lock']
		self.code = info['code']
		self.id = info['id']