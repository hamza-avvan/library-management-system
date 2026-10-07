class Admin:
	def __init__(self, db):
		self.db = db

	def get_by_id(self, admin_id):
		return self.db.query(
			"SELECT * FROM admin WHERE id = %s",
			(admin_id,),
		).fetchone()

	def get_by_email(self, email):
		return self.db.query(
			"SELECT * FROM admin WHERE email = %s",
			(email,),
		).fetchone()