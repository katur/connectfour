import json
import random
import string

import tornado.web
import tornado.websocket

from connectfour.model import (ConnectFourModel, Color, DEFAULT_ROWS,
                               DEFAULT_COLUMNS, DEFAULT_TO_WIN)
from connectfour.pubsub import ModelAction, ViewAction, PubSub


sessions = {}


class Session():
    def __init__(self):
        self.pk = generate_random_string(10)
        self.connections = set()
        sessions[self.pk] = self

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


class SetupHandler(tornado.web.RequestHandler):
    """Page to set up session parameters."""

    def get(self):
        self.render('setup.html', **{
            'title': 'Connect X',
            'default_rows': DEFAULT_ROWS,
            'default_columns': DEFAULT_COLUMNS,
            'default_to_win': DEFAULT_TO_WIN,
        })

    def post(self):
        session = Session()

        # Eventually move this board setup to the session itself
        num_rows = int(self.get_argument('num_rows'))
        num_columns = int(self.get_argument('num_columns'))
        num_to_win = int(self.get_argument('num_to_win'))
        session.pubsub.publish(
            ViewAction.create_board, num_rows, num_columns, num_to_win)

        player_names = [x.strip() for x in
                        self.get_argument('players').split(',')]
        colors = [c for c in Color]

        # Eventually move player creation to the session itself
        for i, name in enumerate(player_names):
            color = colors[i]
            session.pubsub.publish(ViewAction.add_player, name, color)

        session.pubsub.do_queue()

        self.redirect('/session/{}'.format(session.pk))


class SessionHandler(tornado.web.RequestHandler):
    """Page for playing games in a session."""

    def get(self, session_pk):
        model = sessions[session_pk].model

        self.render('game.html', **{
            'title': 'Connect {}'.format(model.get_num_to_win()),
            'num_rows': model.get_num_rows(),
            'num_columns': model.get_num_columns(),
            'num_to_win': model.get_num_to_win(),
        })


class SessionWebSocketHandler(tornado.websocket.WebSocketHandler):
    """WebSockets connection to go with SessionHandler."""

    def open(self, session_pk):
        self.session = sessions[session_pk]
        self.session.connections.add(self)
        print('Connection to {} open (now {} connections)'
              .format(session_pk, len(self.session.connections)))

    def on_close(self):
        self.session.connections.remove(self)

        if not self.session.connections:
            del sessions[self.session.pk]

        print('Connection to {} closing (leaving {} connections, {} sessions)'
              .format(self.session.pk, len(self.session.connections),
                      len(sessions)))

    def on_message(self, message):
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
            print d['message']

        else:
            print 'Received undefined message type: {}'.format(kind)


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(length))
