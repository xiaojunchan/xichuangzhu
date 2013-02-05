from xichuangzhu import conn, cursor

class Collection:

	# get an author's all collections
	@staticmethod
	def get_collections_by_author(authorID):
		query = "SELECT * FROM collection WHERE AuthorID = %d" % authorID
		cursor.execute(query)
		return cursor.fetchall()

