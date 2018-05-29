import uuid


class User:
    def __init__(self, db):
        self.db = db

        # Add user key with auth cookie
        # [TODO] timed life for unregistered users
        self.id = self.db.incr("latest_user_id")
        self.auth = uuid.uuid4().hex
        self.db.hmset(
            'users:' + str(self.id),
            {
                'auth': self.auth
            }
        )

        # Add user to auth map
        self.db.hset('auths', self.auth, self.id)
