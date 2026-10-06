class BookDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "books"

	def delete(self, id):
		q = self.db.query("DELETE FROM @table where id={}".format(id))
		self.db.commit()

		return q


	def getBook(self, id):
		q = self.db.query("select * from @table where id={}".format(id))

		book = q.fetchone()

		print(book)
		return book

	def list(self, availability=1):
		query="select * from @table"
		# Usually when no-admin user query for book
		if availability==1: query= query+"  WHERE availability={}".format(availability)
		
		books = self.db.query(query)
		
		books = books.fetchall()


		return books

	def search_book(self, name, availability=1):
		query="select * from @table where name LIKE '%{}%'".format(name)

		# Usually when no-admin user query for book
		if availability==1: query= query+"  AND availability={}".format(availability)

		q = self.db.query(query)
		books = q.fetchall()
		
		return books