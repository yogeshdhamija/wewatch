from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
import base64
from managers.user import UserManager
from managers.video import VideoManager

class BaseWSHandler(WebSocketHandler):
    @property
    def db(self):
        return self.application.db

    def initialize(self):
        """ Constructor. """
        self.user_manager = UserManager(self.db)
        self.video_manager = VideoManager(self.db)

    def check_user(self, id, auth):
        """ Given an id and auth, checks if the auth matches the id. """
        return self.user_manager.check_auth(id, auth)

class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    def initialize(self):
        """ Constructor. """
        self.user_manager = UserManager(self.db)
        self.video_manager = VideoManager(self.db)
        self.user = self.login()

    def render(self, template, title, args = {}):
        """ Making the render follow our formatting. """
        super(BaseHandler, self).render(template, title=title, args=args)

    def flash(self, message, m_type = "info"):
        """ Stores a "flash" cookie with a message and message type to be
            destroyed upon consumption. """
        self.set_secure_cookie("message", base64.encodestring(message))
        self.set_secure_cookie("message_type", base64.encodestring(m_type))

    def consume_flash(self):
        """ Gets a stored flash cookie and destroys it. """
        message = self.get_secure_cookie("message")
        m_type = self.get_secure_cookie("message_type")
        if not message:
            return None
        message = base64.decodestring(message)
        if not m_type:
            m_type = "info"
        else:
            m_type = base64.decodestring(m_type)

        self.clear_cookie("message")
        self.clear_cookie("message_type")
        return {
            'message': message,
            'message_type': m_type
        }

    def store_auth(self, id):
        """ Stores the user's auth cookie. """
        auth = self.user_manager.get(id, "auth")
        if not auth:
            raise Exception("Failed to store auth cookie. Could not user_manager.get("+str(id)+", '"+str(auth)+"').")
        self.set_secure_cookie("user_auth", auth)

    def login(self):
        """ Returns the current user's data using UserManager's consume_auth, and store the new cookie.
            If the current user doesn't exist, one is created. """
        cookie = self.get_secure_cookie("user_auth")
        if cookie:
            user_id = self.user_manager.consume_auth(cookie)
        if (not cookie) or (not user_id):
            user_id = self.user_manager.create_new()
        self.store_auth(user_id)
        return self.user_manager.get(user_id)

    def logout(self):
        """ Deletes the user's stored cookie, after consuming it for good measure. """
        cookie = self.get_secure_cookie("user_auth")
        if(cookie):
            self.user_manager.consume_auth(cookie)
        self.clear_cookie("user_auth")

    def check_argument(self, argument):
        "Utility method to check if argument exists and isn't blank."
        return ((argument in self.request.arguments) and (self.get_argument(argument) != ''))
