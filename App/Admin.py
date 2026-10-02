from App.Actor import Actor

class Admin(Actor):
	common_properties = ['name', 'email', 'id', 'created_at']
	specific_properties = []

	def __init__(self, AdminDAO):
		self.sess_key = "admin"
		self.dao = AdminDAO
		self.route_url = "/admin/"