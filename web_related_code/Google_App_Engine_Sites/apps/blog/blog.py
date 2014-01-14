import os
import webapp2
import jinja2
import datetime
import urllib2
import logging
import json
import time
from xml.dom import minidom
from datetime import datetime, timedelta

from google.appengine.ext import db
from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def clearmemcache():
	memcache.flush_all()

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def setsinglepost(postid):
	p = BLOGPOST.get_by_id(int(postid))
	if p:
		memcache.set("POST_" + str(postid), (p, datetime.now()) )
	else:
		logging.error("P IS NOT THERE!")
		return False
		
def getsinglepost(postid):
	p = memcache.get("POST_" + str(postid) )
	if p:
		return p
	else:
		setsinglepost(postid)
		return memcache.get("POST_" + str(postid) )
	
def frontposts(updatecache = False):
	posts = memcache.get('front')
	tim = memcache.get('Querytime')
	if posts is None or tim is None or updatecache:
		logging.error('Had to access the database :(')
		posts = db.GqlQuery("SELECT * FROM BLOGPOST ORDER BY created DESC limit 10")
		memcache.set('front', posts)
		memcache.set('Querytime', datetime.now() )
		return list(memcache.get('front')), memcache.get('Querytime')
	else:
		return list(memcache.get('front')), memcache.get('Querytime')
		
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)
		
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class BLOGPOST(db.Model):
	title = db.StringProperty(required=True)
	blogpost = db.TextProperty(required=True)
	created = db.DateProperty(auto_now_add=True)
	
	def render(self):
		self._render_text = self.blogpost.replace('\n', '<br>')
		return render_str('post.html', cont = self)
	
	
class MainPage(Handler):
	def render_front(self, title="", blogpost="", error=""):
		fposts, qtime = frontposts()
		logging.error(str( (qtime - datetime.now() ).total_seconds() ) )
		
		self.render("blog.html", blogposts=fposts, timestamp=("Queried " + str( (datetime.now() - qtime ).total_seconds() ) + " seconds ago"))

	def get(self):
		self.render_front()
			
class NewPost(Handler):
	def render_front(self, title="", blogpost="", error=""):
		self.render("blogpost.html", title=title,blogpost=blogpost,error=error)

	def get(self):
		self.render_front()
		
	def post(self):
		title = self.request.get('subject')
		blogpost = self.request.get('content')
		
		if title and blogpost:
			a = BLOGPOST(title = title, blogpost = blogpost)
			key = a.put()
			time.sleep(1)
			frontposts(updatecache=True)
			logging.error("ERRRRRRRRRRROOORRR " + str(key.id()) )
			setsinglepost(key.id())
			
			self.redirect("/blog/%s" % key.id())
			
		else:
			error = "You need a title AND a blogpost!"
			self.render_front(title, blogpost, error)
			
class idUrl(MainPage):
	def get(self, blog_id):
		#t = BLOGPOST.get_by_id(int(blog_id))
		bp,time = getsinglepost(blog_id) # int
		self.render('specblogpost.html', blogpost=bp, timestamp = ("Queried " + str( ( datetime.now() - time).total_seconds() ) +" seconds ago") )

class MainPageJson(MainPage):
	def getPostInfo(self, id = None):
		dict = {}
		jsonstring = ''
		if id:
			if BLOGPOST.get_by_id(int(id)):
				
				p = BLOGPOST.get_by_id(int(id))
				dict["subject"] = p.title
				dict["created"] = p.created.strftime('%b %d %Y')
				dict["last_modified"] = p.created.strftime('%b %d %Y') # check dis
				dict["content"] = p.blogpost
				logging.error("Called with id param")
				jsonstring = json.dumps(dict)
				return jsonstring
			
			else:
				self.redirect('/blog')
			
		else:	
			allposts = db.GqlQuery('SELECT * FROM BLOGPOST ORDER BY created DESC')
			liposts = []
			logging.error("Blah")
			for p in allposts:
				logging.error("Test" + str(p.key().id()))
				liposts.append(self.getPostInfo(id = p.key().id()) ) # list of dictionaries
	
			jsonstring = json.dumps(liposts)
			return jsonstring
			
	def get(self, id):
		
		if id:
			self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
			self.write(self.getPostInfo(id = id))
		else:
			self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
			self.write(self.getPostInfo())
			
class FlushUrl(Handler):
	def get(self):
		clearmemcache()
		self.redirect('/blog')
			
app = webapp2.WSGIApplication([('/blog', MainPage),
							   ('/blog/newpost', NewPost),
							   ('/blog/?(\d+)*.json', MainPageJson),
							   ('/blog/(\d+)', idUrl),
							   ('/blog/flush', FlushUrl)], debug=True)
		