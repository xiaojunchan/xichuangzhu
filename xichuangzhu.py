# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import MySQLdb

app = Flask(__name__)

conn = MySQLdb.connect(host='localhost', user='root', passwd='xiaowangzi', db='classic', charset='utf8')
cursor = conn.cursor()

# page home
@app.route('/')
def index():
	cursor.execute('SELECT * FROM work')
	works = cursor.fetchall()
	return render_template('index.html', works=works)

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