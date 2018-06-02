from base_handler import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        user_id = self.login()
        if not user_id:
            user_id = self.user_manager.create_new()
            self.store_auth(user_id)

        args = {
            'title': "We Watch",
            'user_info_string': str(self.user_manager.get(user_id)),
        }
        self.render("index.html", args=args)
