import random
import string

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit

from connectfour.model import (
    ConnectFourModel, DEFAULT_ROWS, DEFAULT_COLUMNS, DEFAULT_TO_WIN)
from connectfour.pubsub import ModelAction, ViewAction, PubSub
from connectfour.web.localsettings import DEBUG

ROOM_ID_LENGTH = 4


# Set up application
async_mode = None
app = Flask(__name__)
app.config.update(
    DEBUG=DEBUG,
)
socketio = SocketIO(app, async_mode=async_mode)

# To map user session ids to room
sid_to_room = {}

# To map rooms to room-specific state
room_to_state = {}


class RoomState():
    """Room-specific state, including model and model event handlers."""

    def __init__(self, room):
        self.room = room
        self.pubsub = PubSub()
        self.model = ConnectFourModel(self.pubsub)
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

    def on_game_started(self):
        socketio.emit('gameStarted', {}, room=self.room)

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

    def on_game_won(self, winner, winning_positions):
        socketio.emit('gameWon', {
            'winner': winner.get_json(),
            'players': self.model.get_json_players(),
            'winningPositions': list(sorted(winning_positions)),
        }, room=self.room)

    def on_game_draw(self):
        socketio.emit('gameDraw', {
            'players': self.model.get_json_players(),
        }, room=self.room)


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

    if 'room' in data:
        room = data['room']

        if room not in room_to_state:
            emit('roomDoesNotExist', {
              'room': room,
            })
            return

    else:
        room = _create_new_room()

    join_room(room)
    sid_to_room[request.sid] = room
    room_state = _get_room_state(request)
    model = room_state.model

    emit('roomJoined', {
        'pk': request.sid,
        'room': room,
        'players': model.get_json_players(),
        'board': model.get_json_board(),
    })

    pubsub = room_state.pubsub
    pubsub.publish(
        ViewAction.add_player, trigger_queue=True, name=name, pk=request.sid)


@socketio.on('disconnect')
def on_disconnect():
    try:
        model = _get_room_state(request).model
    except KeyError:
        return

    player = [p for p in model.players if p.pk == request.sid][0]
    pubsub = _get_room_state(request).pubsub
    pubsub.publish(ViewAction.remove_player, trigger_queue=True, player=player)

    room = sid_to_room[request.sid]
    del sid_to_room[request.sid]

    if not model.players:
        del room_to_state[room]


@socketio.on('createBoard')
def on_create_board(data):
    num_rows = int(data['numRows'])
    num_columns = int(data['numColumns'])
    num_to_win = int(data['numToWin'])

    pubsub = _get_room_state(request).pubsub
    pubsub.publish(
        ViewAction.create_board, trigger_queue=True, num_rows=num_rows,
        num_columns=num_columns, num_to_win=num_to_win)


@socketio.on('startGame')
def on_start_game(data):
    # TODO: add error checking
    pubsub = _get_room_state(request).pubsub
    pubsub.publish(ViewAction.start_game, trigger_queue=True)


@socketio.on('play')
def on_play(data):
    # TODO: add error checking (that current player really played)
    column = int(data['column'])
    pubsub = _get_room_state(request).pubsub
    pubsub.publish(ViewAction.play, trigger_queue=True, column=column)


###########
# Helpers #
###########

def _get_room_state(request):
    return room_to_state[sid_to_room[request.sid]]


def _create_new_room():
    room = _get_random_string(ROOM_ID_LENGTH)
    room_to_state[room] = RoomState(room)
    return room


def _get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase)
                   for _ in range(length))
