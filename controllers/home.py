from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.work_model import Work

# Home Controller
#--------------------------------------------------

# page home
@app.route('/')
def index():
	works = Work.get_works()
	return render_template('index.html', works=works)