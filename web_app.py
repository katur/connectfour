import os

import tornado.ioloop
import tornado.web

from connectfour.views.web.view import (
    make_model, SetupHandler, GameHandler, WebSocketHandler)

BASE_DIR = os.path.join(os.path.dirname(__file__ + '/../'))
SETTINGS = {
    'debug': True,
    'static_path': os.path.join(BASE_DIR, 'connectfour/views/web/static'),
    'template_path': os.path.join(BASE_DIR, 'connectfour/views/web/templates'),
}


def make_app(model):
    return tornado.web.Application([
        (r'/', SetupHandler, {'model': model}),
        (r'/game', GameHandler, {'model': model}),
        (r'/game/websocket', WebSocketHandler, {'model': model}),
    ], **SETTINGS)


if __name__ == "__main__":
    model = make_model()
    app = make_app(model)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
