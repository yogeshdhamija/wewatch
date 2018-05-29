from base_handler import BaseHandler

class HomeHandler(BaseHandler):
	def get(self):
		self.db.set('foo', 'Hello, world! Apparently Redis works!')
		string = self.db.get('foo')
		self.write(string)
