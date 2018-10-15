import uuid
from managers.base_manager import BaseManager


class UserManager(BaseManager):
    def __init__(self, db):
        super(UserManager, self).__init__(db)
        self.db.setnx('latest_user_id', 0)
        self.seconds_to_expire = 60 * 60 * 24 * 30

    def create_new(self):
        """ Creates a new user in redis, adds its to the auths hashmap, and returns the id """

        id = []  # the transaction appends id to this list, since it can access it via reference

        # Add user key with auth cookie
        def create_new_user_transaction(pipe):
            id.append(pipe.incr("latest_user_id"))
            auth = uuid.uuid4().hex
            pipe.hmset(
                'users:' + str(id[0]),
                {
                    'id': id[0],
                    'auth': auth
                }
            )
            pipe.hset('auths', auth, id[0])

        self.db.transaction(create_new_user_transaction, "latest_user_id")

        # Give the user timed life
        self.db.expire('users:' + str(id[0]), self.seconds_to_expire)

        return id[0]

    def check_auth(self, id, auth):
        """ Returns true if the auth matches the ID. """

        if (not auth) or (not id):
            return False

        if not self.db.exists("users:"+str(int(id))):
            return False

        id_from_db = self.db.hget('auths', auth)

        if (not id_from_db):
            return False

        return id == id_from_db

    def consume_auth(self, auth):
        """ Return a user's id, given their auth key. Then change their auth key.
        Also, refresh their time to expire if they don't have a username."""

        if not auth:
            return None

        id = self.db.hget('auths', auth)
        if not self.db.exists('users:'+str(id)):
           return None

        if not self.db.hexists('users:'+str(id), 'username'):
            self.db.expire('users:'+str(id), self.seconds_to_expire)

        new_auth = uuid.uuid4().hex
        with self.db.pipeline() as pipe:
            pipe.hdel('auths', auth)
            pipe.hset('users:'+str(id), 'auth', new_auth)
            pipe.hset('auths', new_auth, id)
            pipe.execute()
        return id

    def get(self, id, field=None):
        """ Return a field's value of a user, given their ID. If the field is None, then return all fields and values as a dictionary. """
        if not id:
            return None

        if field:
            return self.db.hget('users:'+str(int(id)), field)

        return self.db.hgetall('users:'+str(int(id)))
