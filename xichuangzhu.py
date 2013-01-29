# -*- coding: utf-8 -*-

from flask import Flask, render_template
import MySQLdb

app = Flask(__name__)

# home page
@app.route('/')
def index():
	#conn = MySQLdb.connect(host='localhost', user='root', passwd='xiaowangzi', db='beforeidie', charset='utf8')
	#cursor = conn.cursor()
	#cursor.execute('SELECT * FROM goals')
	#return cursor.fetchone()[1]
	return render_template('index.html')

# add classic works
@app.route('/add')
def fuckass():
    return '添加作品'

if __name__ == '__main__':
    app.run(debug=True)