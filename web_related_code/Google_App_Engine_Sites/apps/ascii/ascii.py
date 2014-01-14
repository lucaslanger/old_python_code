import os
import webapp2
import jinja2
import time
import logging
from xml.dom import minidom
import urllib2

from google.appengine.ext import db
from google.appengine.api import memcache

logging.basicConfig(filename='logs.log', level=logging.info)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

GMAPS_URL = 'http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&'

def gmaps_img(points):
	markers = '&'.join('markers=%s,%s' % (p.lat, p.lon) for p in points)
	return GMAPS_URL + markers

def get_coordinates(ip):
	ip = '4.2.2.2'
	ip = '23.24.209.141'
	ip_url = 'http://api.hostip.info/?ip='
	url = ip_url + ip
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except URLError:
		return
		
	if content:
		d = minidom.parseString(content).getElementsByTagName('gml:coordinates')
		if d:
			coords = d[0].firstChild.nodeValue
			temp = coords.split('\n')[0]
			temp = temp.split(',')
			return db.GeoPt(temp[1], temp[0])

def topart(update = False):
	key = 'top'
	arts = memcache.get(key)
	if arts is None or update:
		arts = db.GqlQuery("SELECT * FROM ArtWork ORDER BY created DESC")
		memcache.set('top', arts)
		return list(arts)
	else:		
		return arts

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)
		
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
	
class ArtWork(db.Model):
	title = db.StringProperty(required=True)
	asciiart = db.TextProperty(required=True)
	coords = db.GeoPtProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	
class MainPage(Handler):
	def render_front(self, title="", art="", error="", arts=""):
		arts = topart()
		
		points = []
		points = filter(None, (a.coords for a in arts))
		self.write(repr(points))
		img_url = None
		if points:
			img_url = gmaps_img(points)
		self.render("front.html", arttitle=title,art=art,error=error,arts=arts, img_url = img_url)
	def get(self):
		self.write(self.request.remote_addr)
		self.render_front()
		
	def post(self):
		title = self.request.get('title')
		art = self.request.get('art')
		
		error = title, art
		if title and art:
			a = ArtWork(title = title, asciiart = art)
			coords = get_coordinates(self.request.remote_addr)
			if coords:
				a.coords = coords
			a.put()
			time.sleep(1)
			topart(True)
			
			self.redirect("/ascii")
			
		else:
			#error = "we need a title and some artwork"
			self.render_front(title = title, art = art, error = error)
app = webapp2.WSGIApplication([('/ascii', MainPage)], debug=True)
		