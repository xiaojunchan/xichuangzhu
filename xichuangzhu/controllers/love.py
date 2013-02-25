#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json, session

from xichuangzhu import app

from xichuangzhu.models.love_model import Love

# page - my love works
#--------------------------------------------------

@app.route('/mylove')
def my_love():
	works = Love.get_works_by_user_love(session['user_id'])
	return render_template('my_love.html', works=works)