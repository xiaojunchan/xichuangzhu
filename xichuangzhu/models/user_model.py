from xichuangzhu import conn, cursor

class User:

# CHECK
	
	# check user exist
	@staticmethod
	def check_user(userID):
		query = "SELECT * FROM user WHERE UserID = %d" % userID
		cursor.execute(query)
		return cursor.rowcount > 0
