from xichuangzhu import conn, cursor

class Work:

# GET

	# get all works
	@staticmethod
	def get_works():
		query = '''SELECT work.WorkID, work.Title, work.Content, work.AuthorID, work.DynastyID, author.Author, dynasty.Dynasty\n
			FROM work, author, dynasty\n
			WHERE work.AuthorID = author.AuthorID\n
			AND work.DynastyID = dynasty.DynastyID'''
		cursor.execute(query)
		return cursor.fetchall()

	# get an author's all works
	@staticmethod
	def get_works_by_author(authorID):
		query = "SELECT * FROM work WHERE AuthorID=%d" % authorID
		cursor.execute(query)
		return cursor.fetchall()

	# get the number of shi, wen, ci in an author's works
	@staticmethod
	def get_works_num(works):
		worksNum = {'shi':0, 'ci':0, 'wen':0}
		for work in works:
			if work['Type'] == 'shi':
				worksNum['shi'] += 1
			elif work['Type'] == 'ci':
				worksNum['ci'] += 1
			elif work['Type'] == 'wen':
				worksNum['wen'] += 1
		return worksNum