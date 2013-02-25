from xichuangzhu import conn, cursor

class Work:

# GET

	# get a single work
	@staticmethod
	def get_work(workID):
		query = '''SELECT work.WorkID, work.Title, work.Content, work.Introduction AS WorkIntroduction, work.Type, work.AuthorID, work.DynastyID, work.CollectionID, author.Author, dynasty.Dynasty, collection.Collection, collection.Introduction\n
			FROM work, author, dynasty, collection\n
			WHERE work.workID = %d\n
			AND work.AuthorID = author.AuthorID\n
			AND work.DynastyID = dynasty.DynastyID\n
			AND work.collectionID = collection.CollectionID\n''' % workID
		cursor.execute(query)
		return cursor.fetchone()

	# get works by random
	@staticmethod
	def get_works_by_random(worksNum):
		query = '''SELECT work.WorkID, work.Title, work.Content, work.AuthorID, work.DynastyID, author.Author, dynasty.Dynasty\n
			FROM work, author, dynasty\n
			WHERE work.AuthorID = author.AuthorID\n
			AND work.DynastyID = dynasty.DynastyID\n
			ORDER BY RAND()\n
			LIMIT %d''' % worksNum
		cursor.execute(query)
		return cursor.fetchall()

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

	# get an collection's all works
	@staticmethod
	def get_works_by_collection(collectionID):
		query = "SELECT * FROM work WHERE CollectionID = %d" % collectionID
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

# NEW

	# add a work
	@staticmethod
	def add_work(title, content, introduction, authorID, dynastyID, collectionID, type):
		query = '''INSERT INTO work (Title, Content, Introduction, AuthorID, DynastyID, CollectionID, Type)\n
			VALUES ('%s', '%s', %d, %d, %d, '%s')''' % (title, content, introduction, authorID, dynastyID, collectionID, type)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid

# EDIT

	# edit a Work
	@staticmethod
	def edit_work(title, content, introduction, authorID, dynastyID, collectionID, type, workID):
		query = '''UPDATE work SET Title = '%s', Content = '%s', Introduction = '%s', AuthorID = %d, DynastyID = %d, CollectionID = %d, Type = '%s' WHERE WorkID=%d''' % (title, content, introduction, authorID, dynastyID, collectionID, type, workID)
		cursor.execute(query)
		return conn.commit()

# DELETE

	# delete a work
	@staticmethod
	def delete_work(workID):
		query = "DELETE FROM work WHERE WorkID = %d" % workID
		cursor.execute(query)
		return conn.commit()