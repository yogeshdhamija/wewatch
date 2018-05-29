from base_handler import BaseHandler

class HomeHandler(BaseHandler):
	def get(self):
		self.db.set('foo', 'Hello, world! Apparently Redis works!')
		string = self.db.get('foo')
		string += "\n\nHere are all the keys in Redis: "
		string += str(self._get_all_keys())
		self.write(string)
