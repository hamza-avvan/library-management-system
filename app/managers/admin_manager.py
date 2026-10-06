from app.models.admin import Admin

class AdminManager():
	def __init__(self, DAO):
		self.admin = Admin(DAO.db.admin)
		self.dao = self.admin.dao

	def signin(self, email, password):
		admin = self.dao.getByEmail(email)

		if admin is None:
			return False

		admin_pass = admin["password"] # admin pass at 
		if admin_pass != password:
			return False

		return admin
		
	def get(self, id):
		admin = self.dao.getById(id)

		return admin
		
	def signout(self):
		self.admin.signout()
