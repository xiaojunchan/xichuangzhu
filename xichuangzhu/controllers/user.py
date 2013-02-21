from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.user_model import User

import urllib, urllib2

import smtplib

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

	userID = int(info['douban_user_id'])
	accessToken = info['access_token']

	# get userinfo

	if User.check_user(userID):
		# if user exist, set session
		return '1'
	else:
		# if not, create a new user and verify email
		s = smtplib.SMTP('smtp.qq.com', 25)
		s.login('hustlzp@qq.com', 'xiaowang2013qqzi')
		error = s.sendmail('hustlzp@qq.com', '724475543@qq.com', "Subject: Hi from Python\n\nHello.")
		return "s"
		
		url = "https://api.douban.com/v2/user/~me"
		req = urllib2.Request(url)
		req.add_header('Authorization', 'Bearer ' + accessToken)
		response = urllib2.urlopen(req)
		return response.read()
		return '0'
		# User.add_user()
		# return redirect(url_for('home'))

	return info['access_token']