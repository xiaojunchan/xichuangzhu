from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app, conn, cursor

from xichuangzhu.models.work_model import Work
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.collection_model import Collection

import markdown2

# page - single work
#--------------------------------------------------

@app.route('/work/<int:workID>')
def single_work(workID):
	work = Work.get_work(workID)
	work['Content'] = markdown2.markdown(work['Content'])
	return render_template('single_work.html', work=work)

# page - all works
#--------------------------------------------------
@app.route('/works')
def works():
	works = Work.get_works()
	return render_template('works.html', works=works)

# page - add work
#--------------------------------------------------

@app.route('/work/add', methods=['GET', 'POST'])
def add_work():
	if request.method == 'GET':
		return render_template('add_work.html')
	elif request.method == 'POST':
		title        = request.form['title']
		content      = request.form['content']
		authorID     = int(request.form['authorID'])
		dynastyID    = Dynasty.get_dynastyID_by_author(authorID)
		collectionID = int(request.form['collectionID'])
		type = request.form['type']
		newWorkID = Work.add_work(title, content, authorID, dynastyID, collectionID, type)
		return redirect(url_for('single_work', workID=newWorkID))

# page - edit work
#--------------------------------------------------

@app.route('/work/edit/<int:workID>', methods=['GET', 'POST'])
def edit_work(workID):
	if request.method == 'GET':
		work = Work.get_work(workID)
		return render_template('edit_work.html', work=work)
	elif request.method == 'POST':
		title        = request.form['title']
		content      = request.form['content']
		authorID     = int(request.form['authorID'])
		dynastyID    = Dynasty.get_dynastyID_by_author(authorID)
		collectionID = int(request.form['collectionID'])
		type         = request.form['type']
		Work.edit_work(title, content, authorID, dynastyID, collectionID, type, workID)
		return redirect(url_for('single_work', workID=workID))

# proc - delete work
#--------------------------------------------------

# @app.route('/work/delete/<int:workID>', methods=['GET'])
# def delete_work(workID):
# 	Work.delete_work(workID)
# 	return redirect(url_for('index'))

# helper - search authors and their collections in page add work
#--------------------------------------------------

@app.route('/work/search_authors', methods=['POST'])
def get_authors_by_name():
	name = request.form['author']
	authors = Author.get_authors_by_name(name)
	for author in authors:
		author['Collections'] = Collection.get_collections_by_author(author['AuthorID'])
	return json.dumps(authors)

# helper - search the author's collections in page edit work
#--------------------------------------------------
@app.route('/work/search_collections', methods=['POST'])
def get_collections_by_author():
	authorID = int(request.form['authorID'])
	collections = Collection.get_collections_by_author(authorID)
	return json.dumps(collections)
