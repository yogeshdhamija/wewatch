from base_handler import BaseHandler

class LogoutHandler(BaseHandler):
    def get(self):
        self.logout()
        self.flash("Logged out!", "success")
        self.redirect("/")
