class User:
	def __init__(self, db):
		self.db = db

	def list(self):
		return self.db.query(
			"SELECT users.id, users.name, users.email, users.bio, users.mob, "
			"users.lock, users.created_at, COUNT(reserve.book_id) AS books_owned "
			"FROM users LEFT JOIN reserve ON reserve.user_id = users.id "
			"GROUP BY users.id"
		).fetchall()

	def search(self, query, limit, offset):
		search_term = "%{}%".format(query)
		where_clause = "(name LIKE %s OR email LIKE %s OR bio LIKE %s)"
		params = (search_term, search_term, search_term)
		total = self.db.query(
			"SELECT COUNT(*) AS total FROM users WHERE {}".format(where_clause),
			params,
		).fetchone()["total"]
		users = self.db.query(
			"SELECT id, name, email, bio, COALESCE(NULLIF(mob, ''), '0') AS mob, "
			"`lock`, verify, created_at FROM users WHERE {} "
			"ORDER BY id LIMIT %s OFFSET %s".format(where_clause),
			params + (limit, offset),
		).fetchall()
		return users, total

	def get_by_code(self, code):
		return self.db.query(
			"SELECT * FROM users WHERE code = %s",
			(code,),
		).fetchone()

	def get_by_id(self, user_id):
		return self.db.query(
			"SELECT * FROM users WHERE id = %s",
			(user_id,),
		).fetchone()

	def get_by_email(self, email):
		return self.db.query(
			"SELECT * FROM users WHERE email = %s",
			(email,),
		).fetchone()

	def add(self, user):
		cursor = self.db.query(
			"INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
			(user["name"], user["email"], user["password"]),
		)
		self.db.commit()
		return cursor

	def last_insert_id(self):
		return self.db.query("SELECT LAST_INSERT_ID() AS id").fetchone()

	def delete_by_email(self, email):
		cursor = self.db.query(
			"DELETE FROM users WHERE email = %s",
			(email,),
		)
		self.db.commit()
		return cursor

	def update(self, values, user_id):
		allowed_fields = {"name", "email", "password", "bio", "verify", "code", "lock", "mob"}
		if not values or not set(values).issubset(allowed_fields):
			raise ValueError("Unsupported user update fields")

		set_clause = ", ".join("{} = %s".format(field) for field in values)
		cursor = self.db.query(
			"UPDATE users SET {} WHERE id = %s".format(set_clause),
			tuple(values.values()) + (user_id,),
		)
		self.db.commit()
		return cursor