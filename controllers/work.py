from flask import render_template, request, redirect, url_for, json

import markdown2

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from xichuangzhu import app, conn, cursor

# Work Controller
#--------------------------------------------------

# page single work
@app.route('/work/<int:workID>')
def single_work(workID):
	query = '''SELECT work.WorkID, work.Title, work.Content, work.Type, work.AuthorID, work.DynastyID, work.CollectionID, author.Author, dynasty.Dynasty, collection.Collection, collection.Introduction\n
			FROM work, author, dynasty, collection\n
			WHERE work.workID = %d\n
			AND work.AuthorID = author.AuthorID\n
			AND work.DynastyID = dynasty.DynastyID\n
			AND work.collectionID = collection.CollectionID\n''' % workID
	cursor.execute(query)
	work = cursor.fetchone()
	# use markdown to convert
	work['Content'] = markdown2.markdown(work['Content'])
	return render_template('single_work.html', work=work)

# page add work
@app.route('/work/add', methods=['GET', 'POST'])
def add_work():
	if request.method == 'GET':
		return render_template('add_work.html')
	elif request.method == 'POST':
		# get dynasty id
		query = "SELECT DynastyID FROM author WHERE AuthorID = %d" % int(request.form['authorID'])
		cursor.execute(query)
		dynastyID = cursor.fetchone()['DynastyID']
		# insert
		query = '''INSERT INTO work (Title, Content, AuthorID, DynastyID, CollectionID, Type) VALUES ('%s', '%s', %d, %d, %d, '%s')''' % (request.form['title'], request.form['content'], int(request.form['authorID']), dynastyID, int(request.form['collectionID']), request.form['type'])
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('single_work', workID=cursor.lastrowid))

# page edit work
@app.route('/work/edit/<int:workID>', methods=['GET', 'POST'])
def edit_work(workID):
	if request.method == 'GET':
		query = '''SELECT *\n
			FROM work, author, collection\n
			WHERE work.AuthorID = author.AuthorID\n
			AND work.CollectionID = collection.CollectionID\n
			AND work.WorkID = %d''' % workID
		cursor.execute(query)
		work = cursor.fetchone()
		return render_template('edit_work.html', work=work)
	elif request.method == 'POST':
		# get author id
		query = "SELECT DynastyID FROM author WHERE AuthorID = %d" % int(request.form['authorID'])
		cursor.execute(query)
		dynastyID = cursor.fetchone()['DynastyID']
		# edit
		query = '''UPDATE work SET Title = '%s', Content = '%s', AuthorID = %d, DynastyID = %d, CollectionID = %d, Type = '%s'\n
			WHERE WorkID=%d''' % (request.form['title'], request.form['content'], int(request.form['authorID']), dynastyID, int(request.form['collectionID']), request.form['type'], workID)
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('single_work', workID=workID))

# proc delete work
@app.route('/work/delete/<int:workID>', methods=['GET'])
def delete_work(workID):
	query = "DELETE FROM work WHERE WorkID = %d" % workID
	cursor.execute(query)
	conn.commit()
	return redirect(url_for('index'))

# proc search authors
@app.route('/work/add/search_authors', methods=['POST'])
def search_authors_in_add_work():
	query = "SELECT AuthorID, Author FROM author WHERE Author LIKE '%%%s%%'" % request.form['author']
	cursor.execute(query)
	authors = cursor.fetchall()
	# search for each author's collections
	for author in authors:
		query = "SELECT CollectionID, Collection FROM collection WHERE AuthorID = %d" % author['AuthorID']
		cursor.execute(query)
		collection = cursor.fetchall()
		author['Collections'] = collection
	return json.dumps(authors)