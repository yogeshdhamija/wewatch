from base_handler import BaseHandler, BaseWSHandler
from tornado.web import HTTPError
import base64
import json

class NewVideoHandler(BaseHandler):
    def post(self):
        if not self.check_argument("video"):
            self.flash("Please enter a video.", "danger")
            self.redirect("/")

        video_id = self.video_manager.create_new(
            self.user["id"],
            base64.b64encode(self.get_argument("video"))
        )

        self.redirect("/watch/"+str(video_id))

class WatchHandler(BaseHandler):
    def get(self, video_id):
        if not self._is_user_watching_video(video_id):
            raise HTTPError(404)

        self.video_manager.update_watching(video_id)

        args = {}
        args["user"] = self.user
        args["message"] = self.consume_flash()
        args["video"] = self.video_manager.get(video_id)
        args["websocket_url"] = "ws://" + self.request.host + "/watching_websocket"

        self.render("watching.html", "Watching... | WeWatch", args)

    def _is_user_watching_video(self, video_id):
        """ Helper to determine if video_id exists in watching:[USERID]. """
        return video_id in self.video_manager.watching(self.user["id"])

class WatchingWSHandler(BaseWSHandler):
    def open(self):
        self.phase = "AUTH"

    def on_message(self, message):
        parsed_message = json.loads(message)
        if self.phase == "AUTH":
            if any([
                "user_id" not in parsed_message,
                "user_auth" not in parsed_message,
                "video_id" not in parsed_message
            ]):
                self.write_message("ERROR: bad AUTH")
                self.close()

    def on_close(self):
        print("WebSocket closed")
