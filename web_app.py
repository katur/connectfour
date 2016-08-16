from connectfour.views.web.view import app, socketio


if __name__ == '__main__':
    socketio.run(app)
