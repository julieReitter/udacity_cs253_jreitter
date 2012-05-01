import webapp2
import codecs
import cgi

form="""
    <form method="post">
        <h2>Enter Some Text to ROT13</h2>
        <textarea name="text" cols="75" rows="10">%(text)s</textarea>
        <div style="color:red"> %(error)s </div>
        <br>
        <input type="submit">
    </form>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

class rotHandler(webapp2.RequestHandler):       
    def write_form(self, error="", text=""):
        self.response.out.write(form %{"error":error, "text": escape_html(text)})
        
    def get(self):
        self.write_form()
    
    def post(self):
        user_text = self.request.get("text")
        
        if not user_text:
            self.write_form("Please input some text", user_text)
        else:
            user_text = user_text.encode("rot13")
            self.write_form("", user_text)
        
    
app = webapp2.WSGIApplication([('/unit2/hw1', rotHandler)], debug=True)
