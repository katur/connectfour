import os

import tornado.ioloop
import tornado.web
from tornado.options import define, options

from connectfour.views.web.view import (
    SetupHandler, GameHandler, GameWebSocketHandler)

BASE_DIR = os.path.join(os.path.dirname(__file__ + '/../'))

SETTINGS = {
    'debug': True,
    'static_path': os.path.join(BASE_DIR, 'connectfour/views/web/static'),
    'template_path': os.path.join(BASE_DIR, 'connectfour/views/web/templates'),
}

define("port", default=8888, help="run on the given port", type=int)


def make_app():
    return tornado.web.Application([
        (r'/', SetupHandler),
        (r'/game', GameHandler),
        (r'/game/ws', GameWebSocketHandler),
    ], **SETTINGS)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
