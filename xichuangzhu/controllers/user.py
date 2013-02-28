#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json, session

from xichuangzhu import app

from xichuangzhu.models.user_model import User
from xichuangzhu.models.love_model import Love
from xichuangzhu.models.review_model import Review

import urllib, urllib2

import smtplib
from email.mime.text import MIMEText

import hashlib

import re

# proc - login by douban's oauth2.0
@app.route('/login/douban')
def auth():
	code = request.args['code']

	# get access token and userID
	url = "https://www.douban.com/service/auth2/token"
	data = {
		'client_id': '0cf909cba46ce67526eb1d62ed46b35f',
		'client_secret': '4c87a8ef33e6c6be',
		'redirect_uri': 'http://localhost:5000/login/douban',
		'grant_type': 'authorization_code',
		'code': code
	}
	data = urllib.urlencode(data)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	info = eval(response.read())

	user_id = int(info['douban_user_id'])
	access_token = info['access_token']

	# if user exist
	if User.check_user_exist(user_id):
		# if user unactive
		if not User.check_user_active(user_id):
			return redirect(url_for('verify_email_callback', state='unactive'))
		else:
			# set session
			session['user_id'] = user_id
			session['user_name'] = User.get_name(user_id)
			return redirect(url_for('index'))
	# if not exist
	else:
		# get user info
		url = "https://api.douban.com/v2/user/~me"
		req = urllib2.Request(url)
		req.add_header('Authorization', 'Bearer ' + access_token)
		response = urllib2.urlopen(req)
		user_info = eval(response.read().replace('\\', ''))	# remove '\' and convert str to dict

		# add user
		user_id = int(user_info['id'])
		user_name = user_info['name']
		avatar = user_info['avatar']
		signature = user_info['signature']
		desc = user_info['desc']
		location_id = int(user_info['loc_id'])
		location = user_info['loc_name']
		User.add_user(user_id, user_name, avatar, signature, desc, location_id, location)

		# go to the verify email page
		return redirect(url_for('send_verify_email', user_id=user_id))

# page - send verify email
@app.route('/send_verify_email/douban', methods=['GET', 'POST'])
def send_verify_email():
	if request.method == 'GET':
		user_id = int(request.args['user_id'])
		user_name = User.get_name(user_id)
		return render_template('send_verify_email.html', user_id=user_id, user_name=user_name)
	elif request.method == 'POST':
		# email
		f_addr = "hustlzp@qq.com"
		t_addr = request.form['email']

		# user info
		user_id = int(request.form['user_id'])
		user_name = User.get_name(user_id)

		# add this email to user
		User.add_email(user_id, t_addr)

		# gene verify url
		verify_code = hashlib.sha1(user_name).hexdigest()
		verify_url = "http://localhost:5000/verify_email/douban/" + str(user_id) + "/" + verify_code
		msgText = '''<html>
			<h1>点击如下链接激活你在西窗烛的帐号：</h1>
			<a href='%s'>%s</a>
			</html>''' % (verify_url, verify_url)

		msg = MIMEText(msgText, 'html', 'utf-8')
		msg['From'] = f_addr
		msg['To'] = t_addr
		msg['Subject'] = "[西窗烛] 邮箱验证"

		# send email
		s = smtplib.SMTP('smtp.qq.com', 25)
		s.login('hustlzp@qq.com', 'xiaowang2013qqzi')
		s.sendmail('hustlzp@qq.com', t_addr, msg.as_string())

		return redirect(url_for('verify_email_callback', state='send_succ'))

# proc - verify the code and active user
@app.route('/verify_email/douban/<int:user_id>/<verify_code>')
def verify_email(user_id, verify_code):
	user_name = User.get_name(user_id)
	if verify_code == hashlib.sha1(user_name).hexdigest():
		User.active_user(user_id)
		session['user_id'] = user_id
		session['user_name'] = user_name
		return redirect(url_for('verify_email_callback', state='active_succ'))
	else:
		return redirect(url_for('verify_email_callback', state='active_failed'))

# page - show the state of verify
@app.route('/verify_email_callback/douban/')
def verify_email_callback():
	state = request.args['state']
	return render_template('verify_email_callback.html', state=state)

# proc - logout
@app.route('/logout')
def logout():
	session.pop('user_id', None)
	session.pop('user_name', None)
	return redirect(url_for('index'))

# page - personal page
@app.route('/people/<int:user_id>')
def people(user_id):
	people = User.get_people(user_id)
	works = Love.get_works_by_user_love(user_id)
	for work in works:
		work['Content'] = re.sub(r'<([^<]+)>', '', work['Content'])
	reviews = Review.get_reviews_by_user(user_id)
	return render_template('people.html', people=people, works=works, reviews=reviews)
