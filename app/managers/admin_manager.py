from app.authentication.contexts.admin import AdminAuthContext

class AdminManager():
	def __init__(self, dao):
		self.admin = dao.admin
		self.auth = AdminAuthContext()

	def signin(self, email, password):
		admin = self.admin.get_by_email(email)

		if admin is None:
			return False

		admin_pass = admin["password"] # admin pass at 
		if admin_pass != password:
			return False

		return admin
		
	def get(self, id):
		admin = self.admin.get_by_id(id)

		return admin
		
	def signout(self):
		self.auth.signout()
