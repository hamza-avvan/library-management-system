from app.database.database import DB
from app.models.admin import Admin
from app.models.book import Book
from app.models.reservation import Reservation
from app.models.user import User


class DAO:
	def __init__(self, app):
		database = DB(app)
		self.book = Book(database)
		self.reservation = Reservation(database)
		self.user = User(database)
		self.admin = Admin(database)