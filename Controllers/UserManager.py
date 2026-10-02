from App.User import User

class UserManager():
	def __init__(self, DAO):
		self.user = User(DAO.db.user)
		self.book = DAO.db.book

	def list(self):
		user_list = self.user.dao.list()

		return user_list

	def signin(self, email, password):
		user = self.user.dao.getByEmail(email)

		if user is None:
			return False

		user_pass = user['password'] # user pass at 
		if user_pass != password:
			return False
		
		if user['verify'] != 1:
			return "unverify"

		self.user.set(user)
		return user

	def signout(self):
		self.user.signout()
		
	def get(self, id):
		user = self.user.dao.getById(id)

		return user

	def getUserByCode(self, code):
		user = self.user.dao.get({"code": code})

		return user

	def getByEmail(self, email):
		user = self.user.dao.getByEmail(email)

		return user

	def signup(self, name, email, password):
		user = self.getByEmail(email)

		if user is not None:
			return "already_exists"

		user_info = {"name": name, "email": email, "password": password}
		
		new_user = self.user.dao.add(user_info)

		return self.user.dao.last_insert_id()
		
	def get(self, id):
		user = self.user.dao.getById(id)

		return user
		
	def deleteUserByEmail(self, email):
		user = self.user.dao.delete({'email': email})

		return user
	
	def verify(self, id):
		user = self.user.dao.update({'verify', 1}, id)

		return user

	def update_freely(self, user_info, id):
		user = self.user.dao.update(user_info, id)
		
		self.user.set(user_info)

		return user

	def update(self, name, email, password, bio, id):
		user_info = {"name": name, "email": email, "password": password, "bio":bio}
		
		user = self.update_freely(user_info, id)

		return user

	def getBooksList(self, id):
		return self.book.getBooksByUser(id)

	def getUsersByBook(self, book_id):
		return self.user.dao.getUsersByBook(book_id)