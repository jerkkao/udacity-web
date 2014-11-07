import webapp2
import cgi

template = """
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

def rot13(char):
    asc = ord(char)
    if asc <= ord('z') and asc >= ord('a'):
        asc += 13
        if asc > ord('z'):
            asc -= 26
    elif asc <= ord('Z') and asc >= ord('A'):
        asc += 13
        if asc > ord('Z'):
            asc -= 26
    return chr(asc)

def rot_string(s):
    return ''.join(map(rot13,s[:]))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.write_template()

    def post(self):
        text_value = cgi.escape(rot_string(self.request.get("text")))
        self.response.headers['Content-Type'] = 'text/html'
        self.write_template(text_value)

    def write_template(self, text_value=""):
        self.response.write(template % text_value)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13/', MainPage),
], debug=True)
