#!/usr/bin/env python

from connectfour.web.view import app, socketio


if __name__ == '__main__':
    socketio.run(app)
