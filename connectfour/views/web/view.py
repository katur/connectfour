import json
import logging
import random
import string

from flask import Flask, redirect, render_template, request, url_for
from flask_socketio import (SocketIO, send, emit, rooms,
                            join_room, leave_room, close_room)
from wtforms import Form, IntegerField, StringField, validators

from connectfour.model import (ConnectFourModel, Color, DEFAULT_ROWS,
                               DEFAULT_COLUMNS, DEFAULT_TO_WIN)
from connectfour.pubsub import ModelAction, ViewAction, PubSub
from connectfour.views.web.forms import NewGameForm, ExistingGameForm


async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

game_rooms = {}
log = logging.getLogger('log')


def get_color():
    yield [c for c in Color]


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(length))


def log_number_of_rooms():
    log.info('Number of rooms: {}'.format(len(rooms)))


def add_user_and_redirect(form, room):
    username = form.username.data
    color = get_color()
    room.pubsub.publish(ViewAction.add_player, username, color)
    room.pubsub.do_queue()
    return redirect(url_for('game_room', pk=room.pk))


@app.route('/', methods=['POST', 'GET'])
def setup():
    """Page to set up session parameters."""
    new_game_form = NewGameForm(request.form, prefix='new')
    existing_game_form = ExistingGameForm(request.form, prefix='existing')

    if request.method == 'POST' and new_game_form.validate():
        room = GameRoom()
        # TODO: add optional arg to publish to do queue immediately
        room.pubsub.publish(
            ViewAction.create_board,
            new_game_form.num_rows.data,
            new_game_form.num_columns.data,
            new_game_form.num_to_win.data,
        )
        room.pubsub.do_queue()
        return add_user_and_redirect(new_game_form, room)

    elif request.method == 'POST' and existing_game_form.validate():
        pk = existing_game_form.pk.data
        room = game_rooms[pk]
        return add_user_and_redirect(existing_game_form, room)

    # If either no request.POST or errors
    context = {
        'async_mode': async_mode,
        'title': 'Connect X',
        'new_game_form': new_game_form,
        'existing_game_form': existing_game_form,
    }
    return render_template('setup.html', **context)


@app.route('/game/<pk>')
def game_room(pk):
    """Page for playing in a particular room."""

    model = game_rooms[pk].model

    context = {
        'title': 'Connect {}'.format(model.get_num_to_win()),
        'num_rows': model.get_num_rows(),
        'num_columns': model.get_num_columns(),
        'num_to_win': model.get_num_to_win(),
    }
    return render_template('game_room.html', **context)


@socketio.on('connect')
def connect():
    pk = request.sid
    game_room = game_rooms[pk]
    game_room.connections.add(pk)
    log.info('Open connection to {} (now {} connections)'
             .format(pk, len(game_room.connections)))
    log_number_of_rooms()


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)


@socketio.on('disconnect')
def disconnect():
    print 'disconnected'
    '''
    self.session.connections.remove(self)

    if not self.session.connections:
        del game_rooms[self.session.pk]

    log.info('Close connection to {} (now {} connections)'
                .format(self.session.pk, len(self.session.connections)))
    log_number_of_rooms()
    '''


'''
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


@socketio.on('message')
def on_message(message):

    """Handle incoming messages."""
    d = json.loads(message)
    kind = d['kind']

    # Not used yet
    if kind == 'create_board':
        num_rows = int(d['num_rows'])
        num_columns = int(d['num_columns'])
        num_to_win = int(d['num_to_win'])
        self.session.pubsub.publish(
            ViewAction.create_board, num_rows, num_columns, num_to_win)
        self.session.pubsub.do_queue()

    # Not used yet
    elif kind == 'add_player':
        name = d['name']
        color = Color(d['color'])
        self.session.pubsub.publish(ViewAction.add_player, name, color)
        self.session.pubsub.do_queue()

    elif kind == 'start_game':
        self.session.pubsub.publish(ViewAction.start_game)
        self.session.pubsub.do_queue()

    elif kind == 'play':
        column = int(d['column'])
        self.session.pubsub.publish(ViewAction.play, column)
        self.session.pubsub.do_queue()

    elif kind == 'print':
        log.info(d['message'])

    else:
        log.info('Received undefined message type: {}'.format(kind))
'''


class GameRoom():
    def __init__(self):
        self.pk = generate_random_string(10)
        self.connections = set()
        game_rooms[self.pk] = self

        self.pubsub = PubSub()
        self.model = ConnectFourModel(self.pubsub)
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
        for connection in self.connections:
            connection.write_message({
                'kind': 'board_created',
                'board': str(board),
            })

    def on_player_added(self, player):
        for connection in self.connections:
            connection.write_message({
                'kind': 'player_added',
                'player': player.name,
            })

    def on_game_started(self, game_number):
        for connection in self.connections:
            connection.write_message({
                'kind': 'game_started',
                'game_number': game_number,
            })

    def on_next_player(self, player):
        for connection in self.connections:
            connection.write_message({
                'kind': 'next_player',
                'player': player.name,
            })

    def on_try_again(self, player, reason):
        for connection in self.connections:
            connection.write_message({
                'kind': 'try_again',
                'player': player.name,
                'reason': reason.name,
            })

    def on_color_played(self, color, position):
        for connection in self.connections:
            connection.write_message({
                'kind': 'color_played',
                'color': color.name,
                'position': position,
            })

    def on_game_won(self, player, winning_positions):
        for connection in self.connections:
            connection.write_message({
                'kind': 'game_won',
                'player': player.name,
                'winning_positions': list(sorted(winning_positions)),
            })

    def on_game_draw(self):
        for connection in self.connections:
            connection.write_message({
                'kind': 'game-draw',
            })
