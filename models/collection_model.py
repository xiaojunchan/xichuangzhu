from xichuangzhu import conn, cursor

class Collection:

# GET

	# get an author's all collections
	@staticmethod
	def get_collections_by_author(authorID):
		query = "SELECT * FROM collection WHERE AuthorID = %d" % authorID
		cursor.execute(query)
		return cursor.fetchall()

	# get single collection
	@staticmethod
	def get_collection(collectionID):
		query = '''SELECT * FROM collection, author, dynasty\n
			WHERE collection.AuthorID = author.AuthorID\n
			AND author.DynastyID = dynasty.dynastyID
			AND collectionID = %d''' % collectionID
		cursor.execute(query)
		return cursor.fetchone()

# NEW

	# add a collection
	@staticmethod
	def add_collection(collection, authorID, introduction):
		query = '''INSERT INTO collection (Collection, AuthorID, Introduction) VALUES\n
			('%s', %d, '%s')''' % (collection, authorID, introduction)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid


# EDIT

	# edit a collection
	@staticmethod
	def edit_collection(collection, authorID, introduction, collectionID):
		query = '''UPDATE collection SET Collection = '%s', AuthorID = %d, Introduction = '%s'\n
			WHERE CollectionID = %d''' % (collection, authorID, introduction, collectionID)
		cursor.execute(query)
		return conn.commit()

