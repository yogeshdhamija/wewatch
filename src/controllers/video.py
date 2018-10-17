from controllers.base_handler import BaseHandler, BaseWSHandler
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


class JoinHandler(BaseHandler):
    def get(self, invite):
        video_id = self.video_manager.get_video_from_invite(invite)
        if not video_id:
            raise HTTPError(404)

        args = {}
        args["user"] = self.user
        args["message"] = self.consume_flash()
        args["video_id"] = self.video_manager.get(video_id, "id")
        args["video_link"] = self.video_manager.get(video_id, "link")
        args["invite"] = self.video_manager.get(video_id, "invite_key")

        args["websocket_url"] = "ws://" + self.request.host + "/watching_websocket"

        self.render("watching.html", "Watching... | WeWatch", args)


class WatchHandler(BaseHandler):
    def get(self, video_id):
        if not self._is_user_watching_video(video_id):
            raise HTTPError(404)

        self.video_manager.update_watching(video_id)

        args = {}
        args["user"] = self.user
        args["message"] = self.consume_flash()
        args["video_id"] = self.video_manager.get(video_id, "id")
        args["video_link"] = self.video_manager.get(video_id, "link")
        args["invite"] = self.video_manager.get(video_id, "invite_key")

        args["websocket_url"] = "ws://" + self.request.host + "/watching_websocket"

        self.render("watching.html", "Watching... | WeWatch", args)

    def _is_user_watching_video(self, video_id):
        """ Helper to determine if video_id exists in watching:[USERID]. """
        return video_id in self.video_manager.watching(self.user["id"])


class WatchingWSHandler(BaseWSHandler):
    def open(self):
        self.phase = "AUTH"
        self.id = None
        self.time = None
        self.state = None

    def _authenticate(self, msg):
        if any([
            "user_id" not in msg,
            "user_auth" not in msg,
            "video_id" not in msg,
            "invite_key" not in msg,
            not self.check_user(msg["user_id"], msg["user_auth"])
        ]):
            self.close(1008, "Bad Authentication.")

        if all([
            int(msg["video_id"]) not in self.video_manager.watching(msg["user_id"]),
            msg["video_id"] != self.video_manager.get_video_from_invite(msg["invite_key"])
        ]):
            self.close(1008, "Bad Authentication.")

        self.id = msg["video_id"]

        others = self.get_connections(self.id)
        if others:
            self.time = others[0].time
            self.state = others[0].state

        self.add_connection(self.id, self)
        self.phase = "WATCHING"

        self.write_message(json.dumps({
            "time": self.time,
            "state": self.state
        }))

    def _update(self, msg):
        update = False
        if "time" in msg and "state" in msg:
            if self.time is None or self.state is None:
                update = True
            else:
                if any([
                    abs(msg["time"] - self.time) > 0.5,
                    msg["state"] != self.state
                ]):
                    update = True
        if update:
            self.time = msg["time"]
            self.state = msg["state"]
            for ws in self.get_connections(self.id):
                if ws.phase == "WATCHING":
                    ws.write_message(json.dumps({
                        "time": self.time,
                        "state": self.state
                    }))

    def on_message(self, message):
        parsed_message = False

        try:
            parsed_message = json.loads(message)
        except Exception:
            # TODO: Catch error properly
            self.close(1008, "Bad message. Could not parse JSON.")

        if self.phase == "AUTH":
            self._authenticate(parsed_message)
        if self.phase == "WATCHING":
            self._update(parsed_message)

    def on_close(self):
        self.remove_connection(self.id, self)
