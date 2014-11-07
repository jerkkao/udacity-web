import webapp2
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(user_name):
    return USER_RE.match(user_name)

def valid_password(password):
    return PASS_RE.match(password)

def valid_mail(mail_address):
    return MAIL_RE.match(mail_address)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.write_template()

    def post(self):
        user_name = cgi.escape(self.request.get("username"))
        password = cgi.escape(self.request.get("password"))
        verify_password = cgi.escape(self.request.get("verify"))
        mail = cgi.escape(self.request.get("email"))

        user_name_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        if not valid_username(user_name):
            user_name_error = "That's not a valid username."
        if not valid_password(password):
            password_error = "That wasn't a valid password."
        if password != verify_password:
            verify_error = "Your passwords didn't match."
        if mail != "" and not valid_mail(mail):
            email_error = "That's not a valid email."

        if valid_username(user_name) and (mail == "" or valid_mail(mail)) and valid_password(password) and password == verify_password:
            self.redirect("/welcome?username=%s" % user_name)
        else:
            self.write_template(user_name, mail, user_name_error, password_error, verify_error, email_error)

    def write_template(
        self,
        user_name = "",
        email = "",
        user_name_error = "",
        password_error = "",
        verify_error = "",
        email_error = "",
    ):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write( template % {
            "user_name" : user_name,
            "email" : email,
            "user_name_error" : user_name_error,
            "password_error" : password_error,
            "verify_error" : verify_error,
            "email_error" : email_error
            }
        )

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        user_name = cgi.escape(self.request.get("username"))

        if user_name == "":
            self.redirect('/')

        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(welcome_template % user_name)

application = webapp2.WSGIApplication([
    ('/sign_up/', MainPage),
    ('/sign_up/welcome', WelcomePage)
], debug=True)

template = """
<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
    .label {text-align: right}
    .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(user_name)s">
          </td>
          <td class="error">
            %(user_name_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(password_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(verify_error)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(email_error)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

welcome_template="""
<html>
  <head>
    <title>Unit 2 Signup</title>
  </head>

  <body>
    <h2>Welcome, %s!</h2>
  </body>
</html>
"""
