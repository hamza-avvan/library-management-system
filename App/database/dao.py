from app.database.database_dao import DBDAO

class DAO():
	def __init__(self, app):
		self.db = DBDAO(app)