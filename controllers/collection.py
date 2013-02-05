from flask import render_template, request, redirect, url_for, json

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from xichuangzhu import app, conn, cursor

# Collection Controller
#--------------------------------------------------

# page single collection
@app.route('/collection/<int:collectionID>')
def single_collection(collectionID):
	query = '''SELECT * FROM collection, author, dynasty\n
		WHERE collection.AuthorID = author.AuthorID\n
		AND author.DynastyID = dynasty.dynastyID
		AND collectionID = %d''' % collectionID
	cursor.execute(query)
	collection = cursor.fetchone()
	# works
	query = "SELECT * FROM work WHERE CollectionID = %d" % collectionID
	cursor.execute(query)
	works = cursor.fetchall()
	return render_template('single_collection.html', collection=collection, works=works)

# page add collection
@app.route('/collection/add', methods=['POST', 'GET'])
def add_collection():
	if request.method == 'GET':
		return render_template('add_collection.html')
	elif request.method == 'POST':
		query = '''INSERT INTO collection (Collection, AuthorID, Introduction) VALUES\n
			('%s', %d, '%s')''' % (request.form['collection'], int(request.form['authorID']), request.form['introduction'])
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('single_collection', collectionID = cursor.lastrowid))

# proc search authors in add collection
@app.route('/collection/add/search_author', methods=['POST'])
def search_author_in_add_collection():
	query = "SELECT AuthorID, Author FROM author WHERE Author LIKE '%%%s%%'" % request.form['author']
	cursor.execute(query)
	authors = cursor.fetchall()
	return json.dumps(authors)

# page edit collection
@app.route('/collection/edit/<int:collectionID>', methods=['POST', 'GET'])
def edit_collection(collectionID):
	if request.method == 'GET':
		query = '''SELECT * FROM collection, author\n
			WHERE collection.AuthorID = author.AuthorID\n
			AND CollectionID = %d''' % collectionID
		cursor.execute(query)
		collection = cursor.fetchone()
		return render_template('edit_collection.html', collection=collection)
	elif request.method == 'POST':
		query = '''UPDATE collection SET Collection = '%s', AuthorID = %d, Introduction = '%s'\n
			WHERE CollectionID = %d''' % (request.form['collection'], int(request.form['authorID']), request.form['introduction'], collectionID)
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('single_collection', collectionID=collectionID))