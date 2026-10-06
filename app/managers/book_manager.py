class BookManager():
	def __init__(self, DAO):
		self.dao = DAO.db.book

	def list(self, availability=1):
		return self.dao.list(availability)

	def getBook(self, id):
		books = self.dao.getBook(id)

		return books

	def search(self, keyword, availability=1):
		books = self.dao.search_book(keyword, availability)

		return books

	def delete(self, id):
		self.dao.delete(id)