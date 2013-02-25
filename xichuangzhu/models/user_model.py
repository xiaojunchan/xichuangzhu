from xichuangzhu import conn, cursor

class User:

# GET
	
	# get name by id
	@staticmethod
	def get_name(user_id):
		query = "SELECT Name FROM user WHERE UserID = %d" % user_id
		cursor.execute(query)
		return cursor.fetchone()['Name']

	# get people's all info
	@staticmethod
	def get_people(user_id):
		query = "SELECT * FROM user WHERE UserID = %d" % user_id
		cursor.execute(query)
		return cursor.fetchone()

# UPDATE

	# active user
	@staticmethod
	def active_user(userID):
		query = "UPDATE user SET IsActive = 1 WHERE UserID = %d" % userID
		cursor.execute(query)
		return conn.commit()

	# add email to the user
	@staticmethod
	def add_email(user_id, email):
		query = "UPDATE user SET Email = '%s' WHERE UserID = %d" % (email, user_id)
		cursor.execute(query)
		return conn.commit()

# NEW

	# add a new user
	@staticmethod
	def add_user(userID, name, avatar, signature, desc, locationID, location):
		query = '''INSERT INTO user (UserID, Name, Avatar, Signature, Description, LocationID, Location)\n
			VALUES (%d, '%s', '%s', '%s', '%s', %d, '%s')''' % (userID, name, avatar, signature, desc, locationID, location)
		cursor.execute(query)
		return conn.commit()

# CHECK
	
	# check user exist
	@staticmethod
	def check_user_exist(user_id):
		query = "SELECT * FROM user WHERE UserID = %d" % user_id
		cursor.execute(query)
		return cursor.rowcount > 0

	# check user active
	@staticmethod
	def check_user_active(user_id):
		query = "SELECT * FROM user WHERE UserID = %d AND IsActive = 1" % user_id
		cursor.execute(query)
		return cursor.rowcount > 0


