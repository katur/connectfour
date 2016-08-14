import logging
import random
import string

from flask import Flask, render_template, request
from flask_socketio import (SocketIO, send, emit, rooms,
                            join_room, leave_room, close_room)

from connectfour.model import (ConnectFourModel, get_colors, DEFAULT_ROWS,
                               DEFAULT_COLUMNS, DEFAULT_TO_WIN)
from connectfour.pubsub import ModelAction, ViewAction, PubSub


async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

log = logging.getLogger('log')

sid_to_room = {}
room_data = {}


class RoomData():

    def __init__(self, room):
        self.room = room
        self.pubsub = PubSub()
        self.model = ConnectFourModel(self.pubsub)
        self.colors = get_colors()
        self._create_subscriptions()

    def _create_subscriptions(self):
        responses = {
            ModelAction.board_created: self.on_board_created,
            ModelAction.player_added: self.on_player_added,
            ModelAction.game_started: self.on_game_started,
            ModelAction.next_player: self.on_next_player,
            ModelAction.try_again: self.on_try_again,
            ModelAction.color_played: self.on_color_played,
            ModelAction.game_won: self.on_game_won,
            ModelAction.game_draw: self.on_game_draw,
        }

        for action, response in responses.iteritems():
            self.pubsub.subscribe(action, response)

    def on_board_created(self, board):
        socketio.emit('board_created', {
            'num_rows': board.num_rows,
            'num_columns': board.num_columns,
            'num_to_win': board.num_to_win,
        }, room=self.room)

    def on_player_added(self, player):
        socketio.emit('player_added', {
            'player': str(player),
            'room': self.room,
        }, room=self.room)

    def on_game_started(self, game_number):
        socketio.emit('game_started', {
            'game_number': game_number,
        }, room=self.room)

    def on_next_player(self, player):
        socketio.emit('next_player', {
            'player': str(player),
        }, room=self.room)

    def on_try_again(self, player, reason):
        socketio.emit('try_again', {
            'player': str(player),
            'reason': reason.name,
        }, room=self.room)

    def on_color_played(self, color, position):
        socketio.emit('color_played', {
            'color': color.name,
            'position': position,
        }, room=self.room)

    def on_game_won(self, player, winning_positions):
        socketio.emit('game_won', {
            'player': str(player),
            'winning_positions': list(sorted(winning_positions)),
        }, room=self.room)

    def on_game_draw(self):
        socketio.emit('game_draw', {}, room=self.room)


@app.route('/', methods=['POST', 'GET'])
def index():
    """Page to set up session parameters."""
    context = {
        'async_mode': async_mode,
        'DEFAULT_ROWS': DEFAULT_ROWS,
        'DEFAULT_COLUMNS': DEFAULT_COLUMNS,
        'DEFAULT_TO_WIN': DEFAULT_TO_WIN,
    }
    return render_template('index.html', **context)


@socketio.on('message')
def on_message(message):
    print 'received message: {}'.format(message)


@socketio.on('json')
def on_json(json):
    print 'received json: {}'.format(json)


@socketio.on('connect')
def on_connect():
    print '{} has connected to the server'.format(request.sid)


@socketio.on('disconnect')
def on_disconnect():
    print '{} has disconnected from the server'.format(request.sid)


"""
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    sid_to_room[request.sid] = room
    send('{} has entered the room'.format(username), room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send('{} has left the room'.format(username), room=room)
"""


@socketio.on('add_first_player')
def on_add_first_player(data):
    name = data['username']
    room = _get_random_string(5)

    join_room(room)
    sid_to_room[request.sid] = room
    room_data[room] = RoomData(room)

    color = next(room_data[room].colors)
    pubsub = room_data[room].pubsub
    pubsub.publish(ViewAction.add_player, name, color)
    pubsub.do_queue()


@socketio.on('add_player')
def on_add_player(data):
    name = data['username']
    room = data['room']

    join_room(room)
    sid_to_room[request.sid] = room

    color = next(room_data[room].colors)
    pubsub = room_data[room].pubsub
    pubsub.publish(ViewAction.add_player, name, color)
    pubsub.do_queue()


@socketio.on('create_board')
def on_create_board(data):
    num_rows = int(data['num_rows'])
    num_columns = int(data['num_columns'])
    num_to_win = int(data['num_to_win'])

    pubsub = _get_pubsub(request)
    pubsub.publish(ViewAction.create_board, num_rows, num_columns, num_to_win)
    pubsub.do_queue()


@socketio.on('start_game')
def on_start_game(data):
    pubsub = _get_pubsub(request)
    pubsub.publish(ViewAction.start_game)
    pubsub.do_queue()


@socketio.on('play')
def on_play(data):
    column = int(data['column'])
    pubsub = _get_pubsub(request)
    pubsub.publish(ViewAction.play, column)
    pubsub.do_queue()


def _get_pubsub(request):
    return room_data[sid_to_room[request.sid]].pubsub


def _get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(length))
