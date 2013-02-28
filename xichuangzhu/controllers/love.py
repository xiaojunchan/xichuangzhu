#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json, session

from xichuangzhu import app

from xichuangzhu.models.love_model import Love

import re

# page - my love works
#--------------------------------------------------

@app.route('/mylove')
def my_love():
	if not 'user_id' in session:
		return render_template('my_love.html', is_login=False)
	else:
		works = Love.get_works_by_user_love(session['user_id'])	
		for work in works:
			work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
		return render_template('my_love.html', works=works)

# # proc - add love work
# #--------------------------------------------------
# @app.route('/add_love/<int:work_id>')
# def add_love(work_id):
# 	Love.add_love(session['user_id'], work_id)
# 	return redirect()