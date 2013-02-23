from flask import Flask
app = Flask(__name__)

app.secret_key = 'A0ZfwefdefHH!jmN]LWXewfw,RT'

# mysql
import MySQLdb
import MySQLdb.cursors

conn = MySQLdb.connect(host='localhost', user='root', passwd='xiaowangzi', db='classic', use_unicode=True, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
cursor = conn.cursor()

# convert python's encoding to utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import controllers