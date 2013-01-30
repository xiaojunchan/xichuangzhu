# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import MySQLdb
import MySQLdb.cursors

app = Flask(__name__)

conn = MySQLdb.connect(host='localhost', user='root', passwd='xiaowangzi', db='classic', charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
cursor = conn.cursor()

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

# page work
@app.route('/work/<int:workID>')
def work(workID):
	query = '''SELECT work.WorkID, work.Title, work.Content, work.AuthorID, work.DynastyID, author.Author, dynasty.Dynasty
			FROM work, author, dynasty\n
			WHERE work.workID = d%\n
			AND work.AuthorID = author.AuthorID\n
			AND work.DynastyID = dynasty.DynastyID''' % workID
	cursor.execute(query)
	work = cursor.fetchone()
	return work.WorkID

# page author
@app.route('/author')
def author():
	cursor.execute('SELECT * FROM author')
	authors = cursor.fetchall()
	return render_template('author.html', authors=authors)

# page dynasty
@app.route('/dynasty')
def dynasty():
	cursor.execute('SELECT * FROM dynasty')
	dynasties = cursor.fetchall()
	return render_template('dynasty.html', dynasties=dynasties)

# page add works
@app.route('/add_work', methods=['GET', 'POST'])
def add_work():
	if request.method == 'GET':
		return render_template('add_work.html')
	elif request.method == 'POST':
		return '添加作品'

if __name__ == '__main__':
	app.run(debug=True)