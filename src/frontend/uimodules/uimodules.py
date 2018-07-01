from tornado.options import define, options
import tornado.web

class BaseUIModule(tornado.web.UIModule):
    def render_module(self, module, args = {}):
        """ Making the render_string follow our formatting. """
        return self.render_string("../uimodules/{}".format(module), args=args)

class Navbar(BaseUIModule):
    def render(self, user = False):
        args = {
            "user" : user,
        }
        return self.render_module("navbar.html", args)

class Alert(BaseUIModule):
    def render(self, text, mode="danger"):
        args = {
            "text" : text,
            "mode" : mode
        }
        return self.render_module("alert.html", args=args)