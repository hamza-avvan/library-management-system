from app.models.actor import Actor

class User(Actor):
	common_properties = ['name', 'email', 'id', 'created_at', 'bio']
	specific_properties = ['lock', 'code']

	def __init__(self, UserDAO):
		self.dao = UserDAO
		self.sess_key = "user" # session key