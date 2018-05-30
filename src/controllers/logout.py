from base_handler import BaseHandler

class LogoutHandler(BaseHandler):
    def get(self):
        self.logout()
