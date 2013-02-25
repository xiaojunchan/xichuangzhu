from xichuangzhu import conn, cursor

class Love:

# GET

	# get all works loved by user
	@staticmethod
	def get_works_by_user_love(user_id):
		query = '''SELECT work.WorkID, work.Title, work.Content, author.AuthorID, author.Author\n
			FROM love, user, work, author\n
			WHERE love.UserID = %d\n
			AND love.UserID = user.UserID\n
			AND love.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID''' % user_id
		cursor.execute(query)
		return cursor.fetchall()

	# get all users who love a work
	@staticmethod
	def get_users_love_work(work_id):
		query = '''SELECT user.UserID, user.Name, user.Avatar\n
			FROM love, user\n
			WHERE love.WorkID = %d\n
			AND love.UserID = user.UserID\n''' % work_id
		cursor.execute(query)
		return cursor.fetchall()

# NEW
	
	# a user love a work
	@staticmethod
	def add_love(user_id, work_id):
		query = "INSERT INTO love (UserID, WorkID) VALUES (%d, %d)" % (user_id, work_id)
		cursor.execute(query)
		return conn.commit()

# DELETE

	# a user dislove a work
	@staticmethod
	def remove_love(user_id, work_id):
		query = "DELETE FROM love WHERE UserID = %d AND WorkID = %d" % (user_id, work_id)
		cursor.execute(query)
		return conn.commit()


