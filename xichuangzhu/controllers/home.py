from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.work_model import Work
from xichuangzhu.models.author_model import Author
from xichuangzhu.models.dynasty_model import Dynasty
from xichuangzhu.models.review_model import Review

import re

# Home Controller
#--------------------------------------------------

# page home
@app.route('/')
def index():
	works = Work.get_works_by_random(4)
	for work in works:
		work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
		work['Content'] = work['Content'].replace('%', '')
	reviews = Review.get_reviews_by_random(5)
	authors = Author.get_authors_by_random(5)
	dynasties = Dynasty.get_dynasties()
	return render_template('index.html', works=works, reviews=reviews, authors=authors, dynasties=dynasties)