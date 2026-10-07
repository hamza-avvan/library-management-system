from app.authentication.contexts.user import UserAuthContext

class UserManager():
	def __init__(self, dao):
		self.user = dao.user
		self.auth = UserAuthContext()

	def list(self):
		user_list = self.user.list()

		return user_list

	def search(self, query, limit, offset):
		return self.user.search(query, limit, offset)

	def signin(self, email, password):
		user = self.user.get_by_email(email)

		if user is None:
			return False

		user_pass = user['password'] # user pass at 
		if user_pass != password:
			return False
		
		if user['verify'] != 1:
			return "unverify"

		self.auth.set(user)
		return user

	def signout(self):
		self.auth.signout()
		
	def get(self, id):
		user = self.user.get_by_id(id)

		return user

	def getUserByCode(self, code):
		user = self.user.get_by_code(code)

		return user

	def getByEmail(self, email):
		user = self.user.get_by_email(email)

		return user

	def signup(self, name, email, password):
		user = self.getByEmail(email)

		if user is not None:
			return "already_exists"

		user_info = {"name": name, "email": email, "password": password}
		
		new_user = self.user.add(user_info)

		return self.user.last_insert_id()
		
	def get(self, id):
		user = self.user.get_by_id(id)

		return user
		
	def deleteUserByEmail(self, email):
		user = self.user.delete_by_email(email)

		return user
	
	def verify(self, id):
		user = self.user.update({"verify": 1}, id)

		return user

	def update_freely(self, user_info, id):
		user = self.user.update(user_info, id)
		
		self.auth.set(user_info)

		return user

	def update(self, name, email, password, bio, id):
		user_info = {"name": name, "email": email, "password": password, "bio":bio}
		
		user = self.update_freely(user_info, id)

		return user
