from xichuangzhu import conn, cursor

class Product:

# GET

	# get single product
	@staticmethod
	def get_product(product_id):
		query = "SELECT * FROM product WHERE ProductID = %d" % product_id
		cursor.execute(query)
		return cursor.fetchone()

	# get products by num
	@staticmethod
	def get_products(num):
		query = "SELECT * FROM product LIMIT %d" % num
		cursor.execute(query)
		return cursor.fetchall()

# NEW

	# add product
	@staticmethod
	def add_product(product, url, image_url, introduction):
		query = '''INSERT INTO product (Product, Url, ImageUrl, Introduction)\n
			VALUES ('%s', '%s', '%s', '%s')''' % (product, url, image_url, introduction)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid

# EDIT

	# edit product
	@staticmethod
	def edit_product(product_id, product, url, image_url, introduction):
		query = '''UPDATE product SET Product = '%s', Url = '%s', ImageUrl = '%s', Introduction = '%s' WHERE ProductID = %d''' % (product, url, image_url, introduction, product_id)
		cursor.execute(query)
		return conn.commit()