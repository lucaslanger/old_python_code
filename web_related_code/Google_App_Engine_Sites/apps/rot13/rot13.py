import webapp2
import os
import jinja2
import string

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def rot13(text):
    s = text
    rstr = []
    intab = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    outtab = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
    for a in text:
        if a in intab:
            i = intab.index(a)
            rstr.append(outtab[i])
        else:
            rstr.append(a)
    rstr = "".join(rstr)
    return rstr

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)
		
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))		
	
class Rot13(Handler):
    
    def writerot_form(self,plug=""):
        self.render('rot13.html', text = rot13(plug)) #quote = True?
        
    def get(self):
        self.writerot_form()
        
    def post(self):
        texT = self.request.get("text")
        self.writerot_form(texT)
		
app = webapp2.WSGIApplication([('/rot13', Rot13)], debug=True)