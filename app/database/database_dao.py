from copy import copy

from app.database.admin_repository import AdminDAO
from app.database.book_repository import BookDAO
from app.database.reservation_repository import ReservationDAO
from app.database.user_repository import UserDAO

from app.database.database import DB

class DBDAO(DB):
	def __init__(self, app):
		super(DBDAO, self).__init__(app)

		self.book = BookDAO(copy(self))
		self.reservation = ReservationDAO(copy(self))
		self.user = UserDAO(copy(self))
		self.admin = AdminDAO(copy(self))
