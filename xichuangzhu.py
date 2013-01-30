# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import MySQLdb
import MySQLdb.cursors

app = Flask(__name__)

conn = MySQLdb.connect(host='localhost', user='root', passwd='xiaowangzi', db='classic', charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
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
	query = '''SELECT work.WorkID, work.Title, work.Content, work.AuthorID, work.DynastyID, author.Author, dynasty.Dynasty
			FROM work, author, dynasty\n
			WHERE work.workID = %s\n
			AND work.AuthorID = author.AuthorID\n
			AND work.DynastyID = dynasty.DynastyID''' % workID
	cursor.execute(query)
	work = cursor.fetchone()
	return render_template('single_work.html', work=work)

# page add works
@app.route('/add_work', methods=['GET', 'POST'])
def add_work():
	if request.method == 'GET':
		return render_template('add_work.html')
	elif request.method == 'POST':
		return 'proc add work'

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
	query = '''SELECT *\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID\n
			AND author.AuthorID = %s''' % authorID
	cursor.execute(query)
	author = cursor.fetchone()
	return render_template('single_author.html', author=author)

#page add dynasty
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
	if request.method == 'GET':
		return render_template('add_author.html')
	elif request.method == 'POST':
		return 'proc add author'

# Dynasty Controller
#--------------------------------------------------

# page dynasty
@app.route('/dynasty')
def dynasty():
	cursor.execute('SELECT * FROM dynasty')
	dynasties = cursor.fetchall()
	return render_template('dynasty.html', dynasties=dynasties)

# page single dynasty
@app.route('/dynasty/<int:dynastyID>')
def single_dynasty(dynastyID):
	query = "SELECT * FROM dynasty WHERE DynastyID = %s" % dynastyID
	cursor.execute(query)
	dynasty = cursor.fetchone()
	return render_template('single_dynasty.html', dynasty=dynasty)

#page add dynasty
@app.route('/add_dynasty', methods=['GET', 'POST'])
def add_dynasty():
	if request.method == 'GET':
		return render_template('add_dynasty.html')
	elif request.method == 'POST':
		return 'proc add dynasty'

if __name__ == '__main__':
	app.run(debug=True)