# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for

import MySQLdb
import MySQLdb.cursors

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

conn = MySQLdb.connect(host='localhost', user='root', passwd='xiaowangzi', db='classic', use_unicode=1, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
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

# page add work
@app.route('/add_work', methods=['GET', 'POST'])
def add_work():
	if request.method == 'GET':
		return render_template('add_work.html')
	elif request.method == 'POST':
		# get id
		query = "SELECT AuthorID, DynastyID FROM author WHERE Author = '%s'" % request.form['author']
		cursor.execute(query)
		authorInfo = cursor.fetchone()
		# insert
		query = '''INSERT INTO work (Title, Content, AuthorID, DynastyID, Type) VALUES ('%s', '%s', %d, %d, '%s')''' % (request.form['title'], request.form['content'], authorInfo['AuthorID'], authorInfo['DynastyID'], request.form['type'])
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('index'))

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
	# all works
	query = "SELECT * FROM work WHERE AuthorID = %d" % authorID
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
	return render_template('single_author.html', author=author, works=works, worksNum=worksNum)

#page add author
@app.route('/add_author', methods=['GET', 'POST'])
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
		return redirect(url_for('author'))

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
@app.route('/add_dynasty', methods=['GET', 'POST'])
def add_dynasty():
	if request.method == 'GET':
		return render_template('add_dynasty.html')
	elif request.method == 'POST':
		query = '''INSERT INTO dynasty (Dynasty, Introduction, StartYear, EndYear) VALUES
				('%s', '%s', %d, %d)''' % (request.form['dynasty'], request.form['introduction'], int(request.form['startYear']), int(request.form['endYear']))
		cursor.execute(query)
		conn.commit()
		return redirect(url_for('dynasty'))

if __name__ == '__main__':
	app.run(debug=True)