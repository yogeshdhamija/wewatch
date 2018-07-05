from base_handler import BaseHandler
from tornado.web import HTTPError
import base64

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

        self.render("watching.html", "Watching... | WeWatch", args)

    def _is_user_watching_video(self, video_id):
        """ Helper to determine if video_id exists in watching:[USERID]. """
        return video_id in self.video_manager.watching(self.user["id"])
