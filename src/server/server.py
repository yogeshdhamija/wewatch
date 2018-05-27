from tornado.options import define, options
import tornado.ioloop
import tornado.web
import redis

from controllers.home import HomeHandler

class Application(tornado.web.Application):
	def __init__(self, engine, urls, app_settings):
		tornado.web.Application.__init__(self, urls, **app_settings)
		# self.db = scoped_session(sessionmaker(bind=engine))

if __name__ == "__main__":
	define("port", default=8888, help="listen on the given port", type=int)

	tornado.options.parse_config_file("server_options.conf")

	urls = [
		(r"/", HomeHandler),
	]

	app_settings = {}

	engine = None #[TODO]

	app = Application(engine, urls, app_settings)
	app.listen(options.port)
	tornado.ioloop.IOLoop.current().start()
