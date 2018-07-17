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

        # [TODO] Implement:
        args["invite_key"] = "PLACEHOLDER"

        args["websocket_url"] = "ws://" + self.request.host + "/watching_websocket"

        self.render("watching.html", "Watching... | WeWatch", args)

    def _is_user_watching_video(self, video_id):
        """ Helper to determine if video_id exists in watching:[USERID]. """
        return video_id in self.video_manager.watching(self.user["id"])

class WatchingWSHandler(BaseWSHandler):
    def open(self):
        self.phase = "AUTH"

    def _authenticate(self, msg):
        if any([
            "user_id" not in msg,
            "user_auth" not in msg,
            "video_id" not in msg,
            "invite_key" not in msg,
            not self.check_user(msg["user_id"], msg["user_auth"])
        ]):
            self.close(1008, "Bad Authentication.")

        # [TODO] Check if user has rights to the video: either JSON "invite_key" must point to video, or user must own video.


    def on_message(self, message):
        parsed_message = False

        try:
            parsed_message = json.loads(message)
        except:
            self.close(1008, "Bad message. Could not parse JSON.")

        if self.phase == "AUTH":
            self._authenticate(parsed_message)



    def on_close(self):
        print("WebSocket closed")
