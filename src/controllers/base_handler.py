import tornado.web
from managers.user import UserManager

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def initialize(self):
        self.user_manager = UserManager(self.db)

    def render(self, template, title, args = {}):
        """ Making the render follow our formatting. """
        super(BaseHandler, self).render(template, title=title, args=args)

    def store_auth(self, id):
        """ Stores the user's auth cookie. """
        auth = self.user_manager.get(id, "auth")
        if not auth:
            raise Exception("Failed to store auth cookie. Could not user_manager.get("+str(id)+", '"+str(auth)+"').")
        self.set_secure_cookie("user_auth", auth)

    def login(self):
        """ Returns the current user's ID using UserManager's consume_auth, and store the new cookie. """
        cookie = self.get_secure_cookie("user_auth")
        if not cookie:
            return None
        id = self.user_manager.consume_auth(cookie)
        if not id:
            return None
        self.store_auth(id)
        return id

    def logout(self):
        """ Deletes the user's stored cookie, after consuming it for good measure. """
        cookie = self.get_secure_cookie("user_auth")
        if(cookie):
            self.user_manager.consume_auth(cookie)
        self.clear_cookie("user_auth")
