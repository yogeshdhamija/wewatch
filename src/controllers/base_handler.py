import tornado.web
from managers.user import UserManager

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def initialize(self):
        self.user_manager = UserManager(self.db)

    def login(self, id):
        """ Stores the user's auth as a secure cookie. """
        self.set_secure_cookie("user_auth", self.user_manager.get(id, "auth"))

    def get_current_user(self):
        """ Returns the current user's ID using UserManager's consume_auth, and store the new cookie. """
        if(not self.get_secure_cookie("user_auth")):
            return None
        id = self.user_manager.consume_auth(self.get_secure_cookie("user_auth"))
        self.login(id)
        return id

    def logout(self):
        """ Deletes the user's stored cookie, after consuming it for good measure. """
        if(self.get_secure_cookie("user_auth")):
            self.user_manager.consume_auth(self.get_secure_cookie("user_auth"))
        self.clear_cookie("user_auth")
