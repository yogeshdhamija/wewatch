from base_handler import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        id = self.get_current_user()
        if not id:
            string = "Not logged in."
        else:
            string = "<pre>" + str(self.user_manager.get(id)) + "</pre>"
        self.write(string)

class DevLoginHandler(BaseHandler):
    def prepare(self):
        self.logout()
    def get(self):
        self.login(self.get_argument('id'))

class DevLogoutHandler(BaseHandler):
    def get(self):
        self.logout()
