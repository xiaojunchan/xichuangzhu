from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.author_model import Author
from xichuangzhu.models.work_model import Work
from xichuangzhu.models.collection_model import Collection
from xichuangzhu.models.dynasty_model import Dynasty

# page all authors
#--------------------------------------------------

@app.route('/author')
def author():
	dynasties = Dynasty.get_dynasties()
	for dyn in dynasties:
		dyn['authors'] = Author.get_authors_by_dynasty(dyn['DynastyID'])
	return render_template('author.html', dynasties=dynasties)

# page single author
#--------------------------------------------------

@app.route('/author/<int:authorID>')
def single_author(authorID):
	author      = Author.get_author(authorID)
	collections = Collection.get_collections_by_author(authorID)
	works       = Work.get_works_by_author(authorID)
	worksNum    = Work.get_works_num(works)
	return render_template('single_author.html', author=author, collections=collections, works=works, worksNum=worksNum)

# page add author
#--------------------------------------------------

@app.route('/author/add', methods=['GET', 'POST'])
def add_author():
	if request.method == 'GET':
		dynasties = Dynasty.get_dynasties()
		return render_template('add_author.html', dynasties=dynasties)
	elif request.method == 'POST':
		author       = request.form['author']
		introduction = request.form['introduction']
		birthYear    = int(request.form['birthYear'])
		deathYear    = int(request.form['deathYear'])
		dynastyID    = int(request.form['dynastyID'])
		newAuthorID  = Author.add_author(author, introduction, birthYear, deathYear, dynastyID)
		return redirect(url_for('single_author', authorID=newAuthorID))

# page edit author
#--------------------------------------------------

@app.route('/author/edit/<int:authorID>', methods=['GET', 'POST'])
def edit_author(authorID):
	if request.method == 'GET':
		dynasties = Dynasty.get_dynasties()
		author = Author.get_author(authorID)
		return render_template('edit_author.html', dynasties=dynasties, author=author)
	elif request.method == 'POST':
		author       = request.form['author']
		quote        = request.form['quote']
		introduction = request.form['introduction']
		birthYear    = int(request.form['birthYear'])
		deathYear    = int(request.form['deathYear'])
		dynastyID    = int(request.form['dynastyID'])		
		Author.edit_author(author, quote, introduction, birthYear, deathYear, dynastyID, authorID)
		return redirect(url_for('single_author', authorID=authorID))