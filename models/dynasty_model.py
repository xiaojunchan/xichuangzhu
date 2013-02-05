from xichuangzhu import conn, cursor

class Dynasty:

# GET

	# get all dynasties
	@staticmethod
	def get_dynasties():
		query = "SELECT * FROM dynasty ORDER BY StartYear ASC";
		cursor.execute(query)
		return cursor.fetchall()

	# get single dyansty
	@staticmethod
	def get_dynasty(dynastyID):
		query = "SELECT * FROM dynasty WHERE DynastyID = %d" % dynastyID
		cursor.execute(query)
		return cursor.fetchone()

# new

	# add a new dynasty
	@staticmethod
	def add_dynasty(dynasty, introduction, startYear, endYear):
		query = '''INSERT INTO dynasty (Dynasty, Introduction, StartYear, EndYear) VALUES
			('%s', '%s', %d, %d)''' % (dynasty, introduction, startYear, endYear)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid

# EDIT

	# edit a dynasty
	@staticmethod
	def edit_dynasty(dynasty, introduction, startYear, endYear, dynastyID):
		query = '''UPDATE dynasty SET Dynasty='%s', Introduction='%s', StartYear=%d, EndYear=%d\n
			WHERE DynastyID = %d''' % (dynasty, introduction, startYear, endYear, dynastyID)
		cursor.execute(query)
		return conn.commit()
