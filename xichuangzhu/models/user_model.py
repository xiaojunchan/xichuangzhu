from xichuangzhu import conn, cursor

class User:

# CHECK
	
	# check user exist
	@staticmethod
	def check_user(userID):
		query = "SELECT * FROM user WHERE UserID = %d" % userID
		cursor.execute(query)
		return cursor.rowcount > 0

# NEW

	# add a new user
	@staticmethod
	def add_user(userID, name, avatar, signature, desc, locationID, location):
		query = '''INSERT INTO user (UserID, Name, Avatar, Signature, Description, LocationID, Location)\n
			VALUES (%d, '%s', '%s', '%s', '%s', %d, '%s')''' % (userID, name, avatar, signature, desc, locationID, location)
		cursor.execute(query)
		return conn.commit()

