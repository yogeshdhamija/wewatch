from base_handler import BaseHandler

class DevHandler(BaseHandler):
    def get(self):
        # new_video = self.video_manager.create_new(self.user["id"], "https://www.youtube.com/watch?v=bqy4XFraBlk")
        # self.write(self.video_manager.get(new_video))
        self.write("DEV")
