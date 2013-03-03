from xichuangzhu import conn, cursor

class Widget:

# GET

	# get all widgets of a target
	@staticmethod
	def get_widgets(target_type, target_id):
		query = "SELECT * FROM widget WHERE Type = '%s' AND TargetID = %d ORDER BY PositionIndex ASC" % (target_type, target_id)
		cursor.execute(query)
		return cursor.fetchall()

	# get a widget
	@staticmethod
	def get_widget(widget_id):
		query = "SELECT * FROM widget WHERE WidgetID = %d" % widget_id
		cursor.execute(query)
		return cursor.fetchone()

# NEW

	# add new widget to a target
	@staticmethod
	def add_widget(target_type, target_id, title, content, position_index):
		query = '''INSERT INTO widget (Type, TargetID, Title, Content, PositionIndex)\n
			VALUES ('%s', %d, '%s', '%s', %d)''' % (target_type, target_id, title, content, position_index)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid

# EDIT 

	# edit a widget
	@staticmethod
	def edit_widget(widget_id, title, content, position_index):
		query = '''UPDATE widget SET Title = '%s', Content = '%s', PositionIndex = %d\n
			WHERE WidgetID = %d''' % (title, content, position_index, widget_id)
		cursor.execute(query)
		return conn.commit()

# DELETE

	# delete a widget
	@staticmethod
	def delete_widget(widget_id):
		query = "DELETE FROM widget WHERE WidgetID = %d" % widget_id
		cursor.execute()
		return conn.commit()