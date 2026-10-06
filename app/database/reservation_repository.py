class ReservationDAO:
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "reserve"

	def reserve(self, user_id, book_id):
		try:
			updated = self.db.query(
				"UPDATE books SET count = count - 1 WHERE id = %s AND count > 0",
				(book_id,),
			)
			if updated.rowcount == 0:
				self.db.commit()
				return "err_out"

			self.db.query(
				"INSERT INTO @table (user_id, book_id) VALUES (%s, %s)",
				(user_id, book_id),
			)
			self.db.commit()
			return True
		except Exception:
			self.db.mysql.get_db().rollback()
			raise

	def get_books_by_user(self, user_id):
		return self.db.query(
			"SELECT books.* FROM books "
			"INNER JOIN @table ON @table.book_id = books.id "
			"WHERE @table.user_id = %s",
			(user_id,),
		).fetchall()

	def get_books_count_by_user(self, user_id):
		return self.db.query(
			"SELECT COUNT(book_id) AS books_count FROM @table WHERE user_id = %s",
			(user_id,),
		).fetchone()

	def get_reserved_books_by_user(self, user_id):
		return self.db.query(
			"SELECT GROUP_CONCAT(book_id SEPARATOR ',') AS user_books "
			"FROM @table WHERE user_id = %s",
			(user_id,),
		).fetchone()

	def get_users_by_book(self, book_id):
		return self.db.query(
			"SELECT users.* FROM users "
			"INNER JOIN @table ON @table.user_id = users.id "
			"WHERE @table.book_id = %s",
			(book_id,),
		).fetchall()