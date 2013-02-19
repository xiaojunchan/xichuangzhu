from xichuangzhu import conn, cursor

class Author:

# GET

	# get all authors
	@staticmethod
	def get_authors():
		query = '''SELECT *\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID\n
			LIMIT 0, 5'''
		cursor.execute(query)
		return cursor.fetchall()

	# get certain dynasty's authors
	@staticmethod
	def get_authors_by_dynasty(dynastyID):
		query = '''SELECT *\n
			FROM author\n
			WHERE author.DynastyID = %d''' % dynastyID
		cursor.execute(query)
		return cursor.fetchall()

	# get single author info
	@staticmethod
	def get_author(authorID):
		query = '''SELECT *\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID\n
			AND author.AuthorID = %d''' % authorID
		cursor.execute(query)
		return cursor.fetchone()

	# get authors by name
	@staticmethod
	def get_authors_by_name(name):
		query = "SELECT AuthorID, Author FROM author WHERE Author LIKE '%%%s%%'" % name
		cursor.execute(query)
		return cursor.fetchall()

# NEW

	# add a new author and return its AuthorID
	@staticmethod
	def add_author(author, introduction, birthYear, deathYear, dynastyID):
		query = '''INSERT INTO author (Author, Introduction, BirthYear, DeathYear, DynastyID) VALUES\n
			('%s', '%s', %d, %d, %d)''' % (author, introduction, birthYear, deathYear, dynastyID)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid

# EDIT

	# edit an author
	@staticmethod
	def edit_author(author, introduction, birthYear, deathYear, dynastyID, authorID):
		query = '''UPDATE author SET Author='%s', Introduction='%s', BirthYear=%d, DeathYear=%d, DynastyID=%d\n
			WHERE AuthorID = %d''' % (author, introduction, birthYear, deathYear, dynastyID, authorID)
		cursor.execute(query)
		return conn.commit()