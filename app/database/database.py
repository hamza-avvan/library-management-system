import os
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
class DB(object):
	"""Initialize mysql database """
	host = os.environ.get('MYSQL_HOST') or "localhost"
	user = os.environ.get('MYSQL_USER') or "root"
	password = os.environ.get('MYSQL_PASSWORD') or ""
	db = os.environ.get('MYSQL_DB') or "lms"

	def __init__(self, app):
		app.config["MYSQL_DATABASE_HOST"] = self.host;
		app.config["MYSQL_DATABASE_USER"] = self.user;
		app.config["MYSQL_DATABASE_PASSWORD"] = self.password;
		app.config["MYSQL_DATABASE_DB"] = self.db;

		self.mysql = MySQL(app, cursorclass=DictCursor)
		# try:
		# 	run_command("mysql -h {} -u{} -p{} {} -e \"\"".format(self.host, self.user, self.password, self.db))
		# except:
		# 	print("Error")
	
	def cur(self):
		return self.mysql.get_db().cursor()

	def query(self, q, params=None):
		h = self.cur()
		h.execute(q, params)

		return h

	def commit(self):
		self.query("COMMIT;")