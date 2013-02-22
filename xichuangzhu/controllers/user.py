#-*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, json

from xichuangzhu import app

from xichuangzhu.models.user_model import User

import urllib, urllib2

import smtplib
from email.mime.text import MIMEText

import hashlib

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

	if User.check_user(userID):
		# if user exist, set session
		return '1'
	else:
		# if not, create a new user and verify email

		# get user info
		url = "https://api.douban.com/v2/user/~me"
		req = urllib2.Request(url)
		req.add_header('Authorization', 'Bearer ' + accessToken)
		response = urllib2.urlopen(req)

		# remove '\' and convert str to dict
		userInfo = eval(response.read().replace('\\', ''))

		# add user
		userID = int(userInfo['id'])
		name = userInfo['name']
		avatar = userInfo['avatar']
		signature = userInfo['signature']
		desc = userInfo['desc']
		locationID = int(userInfo['loc_id'])
		location = userInfo['loc_name']

		User.add_user(userID, name, avatar, signature, desc, locationID, location)

		# send email
		f_addr = "hustlzp@qq.com"
		t_addr = "724475543@qq.com"

		verify_code = hashlib.sha1(name).hexdigest()
		verify_url = "http://xichuangzhu.com/user/verify_email/" + userID + "/" + verify_code
		msgText = '''<html>
			<h1>点击如下链接激活你在西窗烛的帐号：</h1>
			<a href='%s'>%s</a>
			</html>''' % (verify_url, verify_url)

		msg = MIMEText(msgText, 'html', 'utf-8')
		msg['From'] = f_addr
		msg['To'] = t_addr
		msg['Subject'] = "[西窗烛] 邮箱验证"

		s = smtplib.SMTP('smtp.qq.com', 25)
		s.login('hustlzp@qq.com', 'xiaowang2013qqzi')
		error = s.sendmail('hustlzp@qq.com', '724475543@qq.com', msg.as_string())
		return "success"
		# return redirect(url_for('home'))

#@app.route('/login/douban/<>')
#def verify():