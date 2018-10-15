from controllers.base_handler import BaseHandler


class HomeHandler(BaseHandler):
    def get(self):
        args = {}
        args["user"] = self.user
        args["message"] = self.consume_flash()

        self.render("home.html", "Welcome! | WeWatch", args)
