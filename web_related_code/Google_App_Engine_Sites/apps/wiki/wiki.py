import jinja2
import os
import webapp2
import logging
import time
import re
from utils import *

from google.appengine.ext import db
from google.appengine.api import memcache

template_directory = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_directory), autoescape = True)

def debug_homepath(path):
	if path:
		path = path
	else:
		path = '123456789'
	return path

def set_wiki(path, content):
	memcache.set("WIKI_" + str(path), content )

def get_wiki(path):
	p = memcache.get("WIKI_" + str(path) )
	if p:
		return p
	else:
		logging.error('WIKI ARTICLE NOT FOUND')
		return None
		
def mod_history(path, content):
	hist = get_history(path)
	if hist == None:
		hist = [(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), content)]
	else:
		hist.insert(0, (time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()), content) )
	memcache.set('HISTORY_' + str(path), hist)
	
def get_history(path):
	p = memcache.get('HISTORY_' + str(path) )
	if p:
		return p
	else:
		logging.error('NO HISTORY FOUND')
		return None

class Users(db.Model):
	username = db.StringProperty(required = True)
	password_hash = db.StringProperty(required = True)
	
class Wikis(db.Model):
	path = db.StringProperty(required = True)
	content = db.TextProperty(required = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)
		
	def render_template(self, template, **predefined): # **means that they are predefined ex: render(t, a="foo")
		jinja_template = jinja_env.get_template(template)
		return jinja_template.render(predefined) #different render call than method below
		
	def render(self, template, **kw):
		self.write(self.render_template(template, **kw))
	
class WikiArticle(Handler):
	def isloggedIn(self):
		user_id_str = self.request.cookies.get('user_id')
		if user_id_str and check_secure_val(user_id_str):
			return Users.get_by_id(int(user_id_str.split('|')[0]) ).username
		else:
			return None
			
	def get_content(self, path):
		path = debug_homepath(path)
		wiki_article = get_wiki(path)
		return wiki_article if wiki_article != None else None
		
	def renderfront(self, username="", content=""):
		self.render('wiki.html', username=username, content=content, signup=False, signin=False, edit=False, history=False)
		
	def get(self, path):
		user = self.isloggedIn()
		version_number = self.request.get_all('v')
		logging.error(version_number)
		p = get_history(path)
		
		content = self.get_content(path)
		try:# we try and catch the potential for users to enter versions that dont exist
			c = content if len(version_number)==0 else p[int(version_number[0]) - 1][1]
		except:
			c = content
		if user:
			if content:		
				self.renderfront(username=user, content=c )
			else:
				self.redirect('/wiki/_edit/' + path)
		else:
			if content:
				self.renderfront(username = None, content=c)
			else:
				self.renderfront(username = None)
			
			
class EditArticle(Handler):
	def isloggedIn(self):
		user_id_str = self.request.cookies.get('user_id')
		if user_id_str and check_secure_val(user_id_str):
			return Users.get_by_id(int(user_id_str.split('|')[0]) ).username
		else:
			return None	
			
	def get(self, path):
		user = self.isloggedIn()
		content = get_wiki(debug_homepath(path) )  #HACK
		logging.error(content)
		content = content if content else ""
		logging.error(content +" TAKE2")
		if user:		
			self.render('wiki.html', username=user, content=content, edit=True )
		else:
			self.redirect('/wiki/' + path)
			
	def post(self, path):
		content = self.request.get('content')
		if content: # if you dont submit changes then redirect to currentpage
			path = debug_homepath(path)
			w = Wikis(path = path, content = content) 
			key = w.put()
			time.sleep(1)
		
			set_wiki(path, content)
			mod_history(path, content)
		
		self.redirect('/wiki/' + debug_homepath(path) )
		
class History(Handler):
	def get(self, path):
		newpath = debug_homepath(path)
		history = get_history(newpath)
		if history:
			self.render('wiki.html', hist = True, history = history )
		else:
			self.redirect('/wiki/' + newpath)
			
class Signup(Handler):
	def write_signupform(self,u="",p="",v="",e=""):
		self.render('wiki.html', usrnerror=u, pwerror=p, verror=v, emailerror=e, signup=True)
		
	def get(self):
		self.write_signupform() 	
		
	def post(self):
		usernames = [usr.username for usr in db.GqlQuery('SELECT * FROM Users')]
		username = self.request.get("username") 
		pw = self.request.get("password")
		vpw = self.request.get("verify")
		email = self.request.get("email")
		
		if v_u(username, usernames) & v_pw(pw) & v_vpw(vpw,pw) & v_em(email):
			new_user = Users(username = username, password_hash = make_pw_hash(username, pw) )
			key = new_user.put()
			
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.headers.add_header('Set-Cookie', 'user_id=%s;Path=/' % make_secure_val(str(int(key.id()) ) ) )
			time.sleep(1)
			
			self.redirect('/wiki/')
			
		else:
			ue,pe,ve,ee = "Sorry, that username is taken!" if usrn_taken(username,usernames) else "Invalid Username" ,"Invalid Password","Passwords Don't Match","Invalid Email" 
			self.write_signupform(ue if not(v_u(username,usernames)) else "",  pe if not(v_pw(pw)) else "",  ve if not(v_vpw(vpw,pw)) else "",  ee if not(v_em(email)) else "")

class Signin(Handler):
	def get(self):
		self.render('wiki.html', signin=True)
		
	def post(self):
		info = db.GqlQuery('SELECT * FROM Users')
		rerender = True
	
		username = self.request.get('username')
		password = self.request.get('password')
		
		lerror = "Invalid Login"
		
		for u in info:
			if u.username == username and valid_pw(username, password, u.password_hash):
				logging.error(u.password_hash)
				id = u.key().id()
				self.response.headers['Content-Type'] = 'text/plain'
				self.response.headers.add_header('Set-Cookie', 'user_id=%s;Path=/' % make_secure_val(str(int(id)) ) )
				self.redirect('/wiki/')

		self.render('wiki.html', signin=True , login_error = lerror)
			
class Signout(Handler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.headers.add_header('Set-Cookie', 'user_id=;Path=/')
		self.redirect('/wiki/')

app = webapp2.WSGIApplication([
('/wiki/signup', Signup),
('/wiki/signin', Signin),
('/wiki/signout', Signout),
('/wiki/_edit/(.*)', EditArticle),
('/wiki/_history/(.*)', History),
('/wiki/(.*)', WikiArticle)], debug = True)