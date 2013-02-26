from xichuangzhu import conn, cursor

class Comment:

# GET 

	# get comments by review
	@staticmethod
	def get_comments_by_review(review_id):
		query = '''SELECT comment.CommentID, comment.Comment, comment.Time, user.UserID, user.Name, user.Avatar\n
			FROM comment, user\n
			WHERE comment.UserID = user.UserID
			AND comment.ReviewID = %d''' % review_id
		cursor.execute(query)
		return cursor.fetchall()

# NEW

	# add comment to a review
	@staticmethod
	def add_comment(user_id, review_id, comment, is_root=0, parent_comment_id=0):
		query = '''INSERT INTO comment (UserID, ReviewID, Comment, IsRoot, ParentCommentID)\n
			VALUES (%d, %d, '%s', %d, %d)''' % (user_id, review_id, comment, is_root, parent_comment_id)
		cursor.execute(query)
		return conn.commit()