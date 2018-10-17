import time
import uuid
from managers.base_manager import BaseManager


class VideoManager(BaseManager):
    def __init__(self, db):
        super(VideoManager, self).__init__(db)
        self.db.setnx('latest_video_id', 0)
        self.seconds_to_expire = 60 * 60 * 24 * 30

    def create_new(self, user_id, link):
        """ Creates a new video in redis,
        appends it to the 'watching:[USERID]' sorted set,
        and returns the id. """

        id = []  # the transaction appends id to this list, since it can access it via reference

        # Add video and append its ID and current timestamp to watching sset
        def create_new_video_transaction(pipe):
            id.append(pipe.incr("latest_video_id"))
            invite = uuid.uuid4().bytes.encode("base64").rstrip("=\n").replace('/', '_')
            pipe.hmset(
                'videos:' + str(id[0]),
                {
                    'id': id[0],
                    'link': link,
                    'owner': int(user_id),
                    'time': 0,
                    'invite_key': invite
                }
            )
            pipe.zadd('watching:'+str(int(user_id)), time.time(), id[0])
            pipe.hset('invites', invite, id[0])

        self.db.transaction(create_new_video_transaction, "latest_video_id")

        # Give the video timed life
        self.db.expire('videos:' + str(id[0]), self.seconds_to_expire)

        return id[0]

    def get(self, id, field=None):
        """ Return a field's value of a video, given its ID. If the field is None, then return all fields and values as a dictionary. """
        if not id:
            return None
        if field:
            return self.db.hget('videos:'+str(int(id)), field)
        return self.db.hgetall('videos:'+str(int(id)))

    def watching(self, user_id):
        """ Get video_ids of everything user_id is watching, ordered descending by timestamp. """
        return self.db.zrevrange('watching:'+str(int(user_id)), 0, -1)

    def update_watching(self, id):
        """ Updates the watching score for the video, as well as its timed life. Does not return."""
        self.db.zadd(
            'watching:'+str(self.get(id, 'owner')),
            time.time(),
            int(id)
        )
        self.db.expire('videos:'+str(int(id)), self.seconds_to_expire)

    def get_video_from_invite(self, key):
        """ Gets video id from invite key, or returns None. """
        if not key:
            return None
        id = self.db.hget('invites', key)
        if not self.db.exists('videos:'+str(id)):
            return None
        return id
