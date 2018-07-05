from tornado.options import define, options
import tornado.web
import base64

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
        return self.render_module("alert.html", args)

class NewVideoForm(BaseUIModule):
    def render(self):
        args = {}
        return self.render_module("new_video_form.html", args)

class Watch(BaseUIModule):
    def render(self, video):
        args = {
            "id" : video["id"],
            "link" : base64.b64decode(video["link"])
        }
        return self.render_module("watch_video.html", args)
