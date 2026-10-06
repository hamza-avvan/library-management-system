class ReservationManager:
	def __init__(self, DAO):
		self.dao = DAO.db.reservation

	def reserve_for_user(self, user_id, book_id):
		return self.dao.reserve(user_id, book_id)

	def get_reserved_books_by_user(self, user_id):
		return self.dao.get_reserved_books_by_user(user_id)

	def get_books_for_user(self, user_id):
		return self.dao.get_books_by_user(user_id)

	def get_books_count_for_user(self, user_id):
		return self.dao.get_books_count_by_user(user_id)

	def get_borrowers_for_book(self, book_id):
		return self.dao.get_users_by_book(book_id)