class UserDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "users"


	def list(self):
		users = self.db.query("select @table.id,@table.name,@table.email,@table.bio,@table.mob,@table.lock,@table.created_at,count(reserve.book_id) as books_owned from @table LEFT JOIN reserve ON reserve.user_id=@table.id GROUP BY reserve.user_id").fetchall()

		return users

	def get(self, filters):
		query = "SELECT * FROM @table WHERE "
		conditions = []
		values = []
		
		for key, value in filters.items():
			conditions.append("{} = {}".format(key, self.db.escape_quotes(value)))
			values.append(value)
		
		query += " AND ".join(conditions)
		
		# Execute the query
		q = self.db.query(query)
		
		# Fetch the result
		user = q.fetchone()

		return user

	def getById(self, id):
		q = self.db.query("select * from @table where id='{}'".format(id))

		user = q.fetchone()

		return user

	def getUsersByBook(self, book_id):
		q = self.db.query("select * from @table LEFT JOIN reserve ON reserve.user_id = @table.id WHERE reserve.book_id={}".format(book_id))

		user = q.fetchall()

		return user

	def getByEmail(self, email):
		q = self.db.query("select * from @table where email='{}'".format(email))

		user = q.fetchone()

		return user

	def last_insert_id(self):
		q = self.db.query("select LAST_INSERT_ID() as id")

		user = q.fetchone()

		return user

	def add(self, user):
		name = user['name']
		email = user['email']
		password = user['password']

		q = self.db.query("INSERT INTO @table (name, email, password) VALUES('{}', '{}', '{}');".format(name, email, password))
		self.db.commit()
		
		return q

	def update(self, userinfo, _id):
		# Extract keys and values from the user dictionary
		keys = list(userinfo.keys())

		
		# Create the SET part of the query dynamically
		set_clause = ", ".join([f"{key} = {self.db.escape_quotes(userinfo[key])}" for key in keys])
		
		# Construct the SQL query with the provided table name
		query = f"UPDATE @table SET {set_clause} WHERE id = {self.db.escape_quotes(_id)}"

		# Execute the query
		q = self.db.query(query)
		self.db.commit()
		
		return q