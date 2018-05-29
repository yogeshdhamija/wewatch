import tornado.web

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def _get_all_keys(self):
		"""
		Returns a list of all the keys in the data store.
		WARNING: slow.
		"""
		return self.db.keys('*')
