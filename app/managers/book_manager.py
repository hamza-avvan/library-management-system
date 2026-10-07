class BookManager():
	def __init__(self, dao):
		self.book = dao.book

	def list(self, availability=1):
		return self.book.list(availability)

	def getBook(self, id):
		books = self.book.get_by_id(id)

		return books

	def search(self, keyword, availability=1):
		books = self.book.search(keyword, availability)

		return books

	def delete(self, id):
		self.book.delete(id)