import os

import tornado.ioloop
import tornado.web

from connectfour.views.web.view import (
    SetupHandler, GameHandler, GameWebSocketHandler)

BASE_DIR = os.path.join(os.path.dirname(__file__ + '/../'))

SETTINGS = {
    'debug': True,
    'static_path': os.path.join(BASE_DIR, 'connectfour/views/web/static'),
    'template_path': os.path.join(BASE_DIR, 'connectfour/views/web/templates'),
}


def make_app():
    return tornado.web.Application([
        (r'/', SetupHandler),
        (r'/game', GameHandler),
        (r'/game/ws', GameWebSocketHandler),
    ], **SETTINGS)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
