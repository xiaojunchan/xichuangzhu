from xichuangzhu import conn, cursor

class Review:

# GET

	# get a review
	@staticmethod
	def get_review(review_id):
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.ReviewID = %d\n
			AND review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID''' % review_id
		cursor.execute(query)
		return cursor.fetchone()

	# get reviews by random
	@staticmethod
	def get_reviews_by_random(reviews_num):
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID\n
			ORDER BY RAND()\n
			LIMIT %d''' % reviews_num
		cursor.execute(query)
		return cursor.fetchall()

	# get hot reviews
	@staticmethod
	def get_hot_reviews():
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID\n'''
		cursor.execute(query)
		return cursor.fetchall()	

	# get reviews of a work
	@staticmethod
	def get_reviews_by_work(work_id):
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.WorkID = %d\n
			AND review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID''' % work_id
		cursor.execute(query)
		return cursor.fetchall()

	# get reviews from a user
	@staticmethod
	def get_reviews_by_user(user_id):
		query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
			FROM review, user, work, author\n
			WHERE review.UserID = %d\n
			AND review.UserID = user.UserID\n
			AND review.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID''' % user_id
		cursor.execute(query)
		return cursor.fetchall()

# NEW

	# add a review to a work
	@staticmethod
	def add_review(work_id, user_id, title, content):
		query = '''INSERT INTO review (WorkID, UserID, Title, Content)\n
			VALUES (%d, %d, '%s', '%s')''' % (work_id, user_id, title, content)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid

# EDIT

	# edit a view
	@staticmethod
	def edit_review(review_id, title, content):
		query = '''UPDATE review SET Title = '%s', Content = '%s' WHERE ReviewID = %d''' % (title, content, review_id)
		cursor.execute(query)
		return conn.commit()