# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, json

import MySQLdb
import MySQLdb.cursors

import markdown2

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

conn = MySQLdb.connect(host='localhost', user='root', passwd='xiaowangzi', db='classic', use_unicode=True, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
cursor = conn.cursor()

# Home Controller
#--------------------------------------------------

# page home
@app.route('/')
def index():
	query = '''SELECT work.WorkID, work.Title, work.Content, work.AuthorID, work.DynastyID, author.Author, dynasty.Dynasty\n
			FROM work, author, dynasty\n
			WHERE work.AuthorID = author.AuthorID\n
			AND work.DynastyID = dynasty.DynastyID'''
	cursor.execute(query)
	works = cursor.fetchall()
	return render_template('index.html', works=works)

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

@app.route

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
	
# Author Controller
#--------------------------------------------------

# page authors
@app.route('/author')
def author():
	query = '''SELECT *\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID'''
	cursor.execute(query)
	authors = cursor.fetchall()
	return render_template('author.html', authors=authors)

#page single author
@app.route('/author/<int:authorID>')
def single_author(authorID):
	# author info
	query = '''SELECT *\n
		FROM author, dynasty\n
		WHERE author.DynastyID = dynasty.DynastyID\n
		AND author.AuthorID = %d''' % authorID
	cursor.execute(query)
	author = cursor.fetchone()
	# collections
	query = "SELECT * FROM collection WHERE AuthorID = %d" % author['AuthorID']
	cursor.execute(query)
	collections = cursor.fetchall()
	# works
	query = "SELECT * FROM work WHERE AuthorID=%d" % authorID
	cursor.execute(query)
	works = cursor.fetchall()
	# works number
	worksNum = {'shi':0, 'ci':0, 'wen':0}
	for work in works:
		if work['Type'] == 'shi':
			worksNum['shi'] += 1
		elif work['Type'] == 'ci':
			worksNum['ci'] += 1
		elif work['Type'] == 'wen':
			worksNum['wen'] += 1
	return render_template('single_author.html', author=author, collections=collections, works=works, worksNum=worksNum)

#page add author
@app.route('/author/add', methods=['GET', 'POST'])
def add_author():
	if request.method == 'GET':
		query = "SELECT DynastyID, Dynasty FROM dynasty ORDER BY StartYear ASC";
		cursor.execute(query)
		dynasties = cursor.fetchall()
		return render_template('add_author.html', dynasties=dynasties)
	elif request.method == 'POST':
		query = '''INSERT INTO author (Author, Introduction, BirthYear, DeathYear, DynastyID) VALUES\n
				('%s', '%s', %d, %d, %d)''' % (request.form['author'], request.form['introduction'], int(request.form['birthYear']), int(request.form['deathYear']), int(request.form['dynastyID']))
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('single_author', authorID=cursor.lastrowid))

# page edit author
@app.route('/author/edit/<int:authorID>', methods=['GET', 'POST'])
def edit_author(authorID):
	if request.method == 'GET':
		# dynasties
		query = "SELECT Dynasty, DynastyID from dynasty ORDER BY StartYear ASC"
		cursor.execute(query)
		dynasties = cursor.fetchall()
		# author info
		query = "SELECT * FROM author WHERE AuthorID = %d" % authorID
		cursor.execute(query)
		author = cursor.fetchone()
		return render_template('edit_author.html', dynasties=dynasties, author=author)
	elif request.method == 'POST':
		query = '''UPDATE author SET Author='%s', Introduction='%s', BirthYear=%d, DeathYear=%d, DynastyID=%d\n
			WHERE AuthorID = %d''' % (request.form['author'], request.form['introduction'], int(request.form['birthYear']), int(request.form['deathYear']), int(request.form['dynastyID']), authorID)
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('single_author', authorID=authorID))

# Dynasty Controller
#--------------------------------------------------

# page dynasty
@app.route('/dynasty')
def dynasty():
	cursor.execute('SELECT * FROM dynasty ORDER BY StartYear ASC')
	dynasties = cursor.fetchall()
	return render_template('dynasty.html', dynasties=dynasties)

# page single dynasty
@app.route('/dynasty/<int:dynastyID>')
def single_dynasty(dynastyID):
	query = "SELECT * FROM dynasty WHERE DynastyID = %d" % dynastyID
	cursor.execute(query)
	dynasty = cursor.fetchone()
	# authors
	query = "SELECT * FROM author WHERE DynastyID = %d" % dynastyID
	cursor.execute(query)
	authors = cursor.fetchall()
	return render_template('single_dynasty.html', dynasty=dynasty, authors=authors)

#page add dynasty
@app.route('/dynasty/add', methods=['GET', 'POST'])
def add_dynasty():
	if request.method == 'GET':
		return render_template('add_dynasty.html')
	elif request.method == 'POST':
		query = '''INSERT INTO dynasty (Dynasty, Introduction, StartYear, EndYear) VALUES
				('%s', '%s', %d, %d)''' % (request.form['dynasty'], request.form['introduction'], int(request.form['startYear']), int(request.form['endYear']))
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('single_dynasty', dynastyID=cursor.lastrowid))

#page edit dynasty
@app.route('/dynasty/edit/<int:dynastyID>', methods=['GET', 'POST'])
def edit_dynasty(dynastyID):
	if request.method == 'GET':
		query = "SELECT * FROM dynasty WHERE DynastyID = %d" % dynastyID
		cursor.execute(query)
		dynasty = cursor.fetchone()
		return render_template('edit_dynasty.html', dynasty=dynasty)
	elif request.method == 'POST':
		query = '''UPDATE dynasty SET Dynasty='%s', Introduction='%s', StartYear=%d, EndYear=%d\n
			WHERE DynastyID = %d''' % (request.form['dynasty'], request.form['introduction'], int(request.form['startYear']), int(request.form['endYear']), dynastyID)
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('single_dynasty', dynastyID=dynastyID))

if __name__ == '__main__':
	app.run(debug=True)