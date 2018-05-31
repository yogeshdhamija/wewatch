from base_handler import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        user_id = self.login()
        if not user_id:
            user_id = self.user_manager.create_new()
            self.store_auth(user_id)

        string = "<pre>" + str(self.user_manager.get(user_id)) + "</pre><br><br><br>"
        args = {
            'title': "We Watch",
            'user_info_string': string,
        }
        self.render("home.html", args=args)
