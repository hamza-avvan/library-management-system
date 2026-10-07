class Book:
	def __init__(self, db):
		self.db = db

	def delete(self, book_id):
		cursor = self.db.query(
			"DELETE FROM books WHERE id = %s",
			(book_id,),
		)
		self.db.commit()
		return cursor

	def get_by_id(self, book_id):
		return self.db.query(
			"SELECT * FROM books WHERE id = %s",
			(book_id,),
		).fetchone()

	def list(self, availability=1):
		query = "SELECT * FROM books"
		params = None
		if availability == 1:
			query += " WHERE availability = %s"
			params = (availability,)
		return self.db.query(query, params).fetchall()

	def search(self, name, availability=1):
		query = "SELECT * FROM books WHERE name LIKE %s"
		params = ("%{}%".format(name),)
		if availability == 1:
			query += " AND availability = %s"
			params += (availability,)
		return self.db.query(query, params).fetchall()