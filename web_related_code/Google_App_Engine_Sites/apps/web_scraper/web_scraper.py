import webapp2
import jinja2
import os

from articles import *

template_directory = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_directory), autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)
		
	def render_page(self, page, **args):
		jinja_page = jinja_env.get_template(page)
		return jinja_page.render(args)
		
	def render(self, page, **args):
		self.write(self.render_page(page, **args))

class HomePage(Handler):
	def getArticles(self, path):
		articles = []
		a = open(path, 'r')
		lines = a.readlines()
		for l in lines:
			cutup = l.split(',')
			articles.append( [cutup[1], cutup[2], cutup[3]] )
		return articles

	def get(self):
		self.render('index.html', articles = article_array)


app = webapp2.WSGIApplication([
('/', HomePage)
])