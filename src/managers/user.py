import uuid


class UserManager:
    def __init__(self, db):
        self.db = db
        self.db.setnx('latest_user_id', 0)

    def create_new(self):
        """ Creates a new user in redis, adds its to the auths hashmap, and returns the id """

        # Add user key with auth cookie
        # [FUTURE] timed life (since these users are not registered yet)
        # [FUTURE] pipeline
        id = self.db.incr("latest_user_id")
        auth = uuid.uuid4().hex
        self.db.hmset(
            'users:' + str(id),
            {
                'id': id,
                'auth': auth
            }
        )

        # Add user to auth map
        self.db.hset('auths', auth, id)

        return id

    def consume_auth(self, auth):
        """ Return a user's id, given their auth key. Then change their auth key. """
        if not auth:
            raise Exception("Cannot UserManager.consume_auth('" + str(auth) + "')")

        # [FUTURE] pipeline
        id = self.db.hget('auths', auth)
        self.db.hdel('auths', auth)
        new_auth = uuid.uuid4().hex
        self.db.hset('users:'+str(id), 'auth', new_auth)
        self.db.hset('auths', new_auth, id)
        return id

    def get(self, id, field=None):
        """ Return a field's value of a user, given their ID. If the field is None, then return all fields and values as a dictionary. """
        if not id:
            raise Exception("Cannot UserManager.get('" + str(id) + "')")
        if field:
            return self.db.hget('users:'+str(id), field)
        return self.db.hgetall('users:'+str(id))
