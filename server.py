#!/usr/bin/python
#prepare
#apt-get install python-pip
#apt-get install python-mysqldb
#pip install flask

from flask import Flask
from flask import render_template
import MySQLdb
import HTMLParser

site = {'name':'TOPTRY','domain':'www.toptry.net','user':'yaoyongqin'}
parser = HTMLParser.HTMLParser()
app = Flask(__name__)


@app.route('/')
def get_list():
	try:
		Db = MySQLdb.connect(host='127.0.0.1', port=3306,user='root',passwd='',db='wordpress', charset='utf8')
	except MySQLdb.Error,e :
		return str("connect to db failed! error %d: %s" % (e.args[0], e.args[1]))
	cmd = "select ID,post_title from wp_posts where post_type='post' order by post_date desc"
	try:
		Cursor = Db.cursor()
		Cursor.execute(cmd)
		result = Cursor.fetchall()
		Cursor.close()
	except:
		return "Get articles fail!"
	articles = []
	for row in result:
		post = {}
		post['url']="http://%s/article/%d" % (site['domain'],int(row[0]))
		post['title'] = row[1]
		articles.append(post)
	return render_template("list.html", site=site, posts = articles)


@app.route('/article/<id>')
def read(id):
	try:
		Db = MySQLdb.connect(host='127.0.0.1', port=3306,user='root',passwd='',db='wordpress', charset='utf8')
	except MySQLdb.Error,e :
		return str("connect to db failed! error %d: %s" % (e.args[0], e.args[1]))
	if id==None:
		return getall()
	cmd = "select post_title, post_content from wp_posts where ID=%d" % int(id)
	try:
		Cursor = Db.cursor()
		Cursor.execute(cmd)
		result = Cursor.fetchone()
		Cursor.close()
		#return parser.unescape(render_template("article.html",user="yao",title=result[0],article=result[1].replace("\n","<br>")))
		return parser.unescape(render_template("index.html",title=result[0],content=result[1].replace("\n","<br>")))
	except:
		return parser.unescape(render_template("index.html",title="Sorry",content="Get article error!"))

@app.route('/photo')
def get_photos():
	return "not support now. please wait..."

@app.route('/test')
def hello_world():
	return 'Hello World! Website@Flask'

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=80,debug=True)
