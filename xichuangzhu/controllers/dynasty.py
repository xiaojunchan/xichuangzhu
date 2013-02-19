from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author

# page all dynasties
#--------------------------------------------------

@app.route('/dynasty')
def dynasty():
	dynasties = Dynasty.get_dynasties()
	return render_template('dynasty.html', dynasties=dynasties)

# page single dynasty
#--------------------------------------------------

@app.route('/dynasty/<int:dynastyID>')
def single_dynasty(dynastyID):
	dynasty = Dynasty.get_dynasty(dynastyID)
	authors = Author.get_authors_by_dynasty(dynastyID)
	return render_template('single_dynasty.html', dynasty=dynasty, authors=authors)

# page add dynasty
#--------------------------------------------------
@app.route('/dynasty/add', methods=['GET', 'POST'])
def add_dynasty():
	if request.method == 'GET':
		return render_template('add_dynasty.html')
	elif request.method == 'POST':
		dynasty      = request.form['dynasty']
		introduction = request.form['introduction']
		startYear    = int(request.form['startYear'])
		endYear      = int(request.form['endYear'])
		newDynastyID = Dynasty.add_dynasty(dynasty, introduction, startYear, endYear)
		return redirect(url_for('single_dynasty', dynastyID=cursor.lastrowid))

# page edit dynasty
#--------------------------------------------------
@app.route('/dynasty/edit/<int:dynastyID>', methods=['GET', 'POST'])
def edit_dynasty(dynastyID):
	if request.method == 'GET':
		dynasty = Dynasty.get_dynasty(dynastyID)
		return render_template('edit_dynasty.html', dynasty=dynasty)
	elif request.method == 'POST':
		dynasty      = request.form['dynasty']
		introduction = request.form['introduction']
		startYear    = int(request.form['startYear'])
		endYear      = int(request.form['endYear'])
		Dynasty.edit_dynasty(dynasty, introduction, startYear, endYear, dynastyID)
		return redirect(url_for('single_dynasty', dynastyID=dynastyID))