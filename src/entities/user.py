import uuid

class User():
	def __init__(self, db):
		self.db = db
		self.db.setnx('latest_user_id', 0)
		self.db.hmset(
			'users:' + str(self.db.incr("latest_user_id")),
			{
				'auth': uuid.uuid4().hex
			}
		)
