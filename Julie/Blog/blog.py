import webapp2
import codecs
import cgi
import os
import urllib
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def escape_html(s):
    return cgi.escape(s, quote = True)

#Database Init
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    date = db.DateTimeProperty(auto_now_add = True)

#template formatting
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
#Page Handlers
class blogHandler(Handler):
    def query_posts(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY date DESC")
        self.render("layout.html", posts=posts, page="all")
        
    def get(self):
        self.query_posts()
           
    
class postHandler(Handler):
    def write_form(self, error="", subject="", content=""):
        self.render("form.html", error=error, subject=subject, content=content)

    def get(self):
        self.write_form()
    
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            q = Post(subject = subject, content = content)
            q.put()
            q_id = q.key().id()
            self.redirect('/blog/%s' %str(q_id))
        else:
            error = "Please Enter Both A Subject & Some Content"
            self.write_form(error = error, subject = subject, content = content)

class permalinkHandler(Handler):   
    def get(self, resource):
        blog_entry = Post.get_by_id(int(resource))
        self.render ("layout.html", post=blog_entry, page="single")

app = webapp2.WSGIApplication([('/blog/newpost', postHandler),
                                ('/blog', blogHandler),
                                (r'/blog/(\d+)', permalinkHandler)], debug=True)


