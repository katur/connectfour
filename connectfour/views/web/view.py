import random
import string

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit

from connectfour.model import (
    ConnectFourModel, get_colors, DEFAULT_ROWS, DEFAULT_COLUMNS,
    DEFAULT_TO_WIN)
from connectfour.pubsub import ModelAction, ViewAction, PubSub
from connectfour.views.web.localsettings import DEBUG, SECRET_KEY

ROOM_ID_LENGTH = 5


# Set up application
async_mode = None
app = Flask(__name__)
app.config.update(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
)
socketio = SocketIO(app, async_mode=async_mode)

# To map user session ids to room
sid_to_room = {}

# To map rooms to room-specific data
room_to_data = {}


class RoomData():
    """Room-specific data, including model and model event handlers."""

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
            ModelAction.player_removed: self.on_player_removed,
            ModelAction.game_started: self.on_game_started,
            ModelAction.next_player: self.on_next_player,
            ModelAction.try_again: self.on_try_again,
            ModelAction.color_played: self.on_color_played,
            ModelAction.game_won: self.on_game_won,
            ModelAction.game_draw: self.on_game_draw,
        }

        for action, response in responses.iteritems():
            self.pubsub.subscribe(action, response)

    def on_player_added(self, player):
        socketio.emit('playerAdded', {
            'player': player.get_json(),
        }, room=self.room)

    def on_player_removed(self, player):
        socketio.emit('playerRemoved', {
            'player': player.get_json(),
        }, room=self.room)

    def on_board_created(self, board):
        socketio.emit('boardCreated', {
            'board': board.get_json(),
        }, room=self.room)

    def on_game_started(self, game_number):
        socketio.emit('gameStarted', {
            # Send along board to ease reset
            'board': self.model.board.get_json(),
            'gameNumber': game_number,
        }, room=self.room)

    def on_next_player(self, player):
        socketio.emit('nextPlayer', {
            'player': player.get_json(),
        }, room=self.room)

    def on_try_again(self, player, reason):
        socketio.emit('tryAgain', {
            'player': player.get_json(),
            'reason': reason.name,
        }, room=self.room)

    def on_color_played(self, color, position):
        socketio.emit('colorPlayed', {
            'color': color.name,
            'position': position,
        }, room=self.room)

    def on_game_won(self, player, winning_positions):
        socketio.emit('gameWon', {
            'player': player.get_json(),
            'winningPositions': list(sorted(winning_positions)),
        }, room=self.room)

    def on_game_draw(self):
        socketio.emit('gameDraw', {}, room=self.room)


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


@socketio.on('addUser')
def on_add_user(data):
    name = data['username']

    if 'room' in data and data['room']:
        room = data['room']
    else:
        room = _create_new_room()

    join_room(room)
    sid_to_room[request.sid] = room
    room_data = _get_room_data(request)
    model = room_data.model

    emit('roomJoined', {
        'pk': request.sid,
        'username': name,
        'room': room,
        'players': [player.get_json() for player in model.players],
        'board': model.board.get_json() if model.board else None,
    })

    color = next(room_data.colors)
    pubsub = room_data.pubsub
    pubsub.publish(
        ViewAction.add_player, name=name, color=color, pk=request.sid)
    pubsub.do_queue()


@socketio.on('disconnect')
def on_disconnect():
    try:
        model = _get_room_data(request).model
    except KeyError:
        return

    player = [p for p in model.players if p.pk == request.sid][0]
    pubsub = _get_room_data(request).pubsub
    pubsub.publish(ViewAction.remove_player, player=player)
    pubsub.do_queue()


@socketio.on('createBoard')
def on_create_board(data):
    # TODO: add error checking
    num_rows = int(data['numRows'])
    num_columns = int(data['numColumns'])
    num_to_win = int(data['numToWin'])

    pubsub = _get_room_data(request).pubsub
    pubsub.publish(
        ViewAction.create_board, num_rows=num_rows, num_columns=num_columns,
        num_to_win=num_to_win)
    pubsub.do_queue()


@socketio.on('startGame')
def on_start_game(data):
    # TODO: add error checking
    pubsub = _get_room_data(request).pubsub
    pubsub.publish(ViewAction.start_game)
    pubsub.do_queue()


@socketio.on('play')
def on_play(data):
    # TODO: add error checking (that current player really played)
    column = int(data['column'])
    pubsub = _get_room_data(request).pubsub
    pubsub.publish(ViewAction.play, column=column)
    pubsub.do_queue()


###########
# Helpers #
###########

def _get_room_data(request):
    return room_to_data[sid_to_room[request.sid]]


def _create_new_room():
    room = _get_random_string(ROOM_ID_LENGTH)
    room_to_data[room] = RoomData(room)
    return room


def _get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(length))
