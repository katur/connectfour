import json

import tornado.web
import tornado.websocket

from connectfour import pubsub
from connectfour.model import (ConnectFourModel, Color, DEFAULT_ROWS,
                               DEFAULT_COLUMNS, DEFAULT_TO_WIN)
from connectfour.pubsub import ModelAction, ViewAction, publish, subscribe


class SetupHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('setup.html', **{
            'title': 'Connect X',
            'default_rows': DEFAULT_ROWS,
            'default_columns': DEFAULT_COLUMNS,
            'default_to_win': DEFAULT_TO_WIN,
        })


class GameHandler(tornado.web.RequestHandler):

    def get(self):
        num_rows = int(self.get_argument('num_rows'))
        num_columns = int(self.get_argument('num_columns'))
        num_to_win = int(self.get_argument('num_to_win'))
        players = [x.strip() for x in self.get_argument('players').split(',')]
        colors = [c.name for c in Color]

        self.render('game.html', **{
            'title': 'Connect {}'.format(num_to_win),
            'num_rows': num_rows,
            'num_columns': num_columns,
            'num_to_win': num_to_win,
            'players': players,
            'colors': colors,
        })


class GameWebSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        self.model = ConnectFourModel()
        self._create_subscriptions()
        super(GameWebSocketHandler, self).__init__(*args, **kwargs)

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
            subscribe(action, response)

    def on_board_created(self, board):
        self.write_message('Created board')

    def on_player_added(self, player):
        self.write_message('Added player {}'.format(player))

    def on_game_started(self, game_number):
        self.write_message('Started game {}'.format(game_number))

    def on_next_player(self, player):
        self.write_message('Player {} next'.format(player))

    def on_try_again(self, player, reason):
        self.write_message('Player {} try again ({})'.format(
            player.name, reason))

    def on_color_played(self, color, position):
        self.write_message('{} played in position {}'.format(
            color, position))

    def on_game_won(self, player, winning_positions):
        self.write_message('{} won the game ({})'.format(
            player, winning_positions))

    def on_game_draw(self):
        self.write_message('Game ended in draw.')

    def on_message(self, message):
        """Handle incoming messages."""
        d = json.loads(message)
        kind = d['kind']

        if kind == 'create_board':
            num_rows = int(d['num_rows'])
            num_columns = int(d['num_columns'])
            num_to_win = int(d['num_to_win'])
            publish(ViewAction.create_board, num_rows, num_columns, num_to_win)
            pubsub.trigger()

        elif kind == 'add_player':
            name = d['name']
            color = Color[d['color']]
            is_ai = False
            publish(ViewAction.add_player, name, color, is_ai)
            pubsub.trigger()

        elif kind == 'start_game':
            publish(ViewAction.start_game)
            pubsub.trigger()

        elif kind == 'play':
            column = int(d['column'])
            publish(ViewAction.play, column)
            pubsub.trigger()

        elif kind == 'print':
            print 'Received message: {}'.format(d['message'])

        else:
            raise Exception('Undefined message type: {}'.format(kind))

    def on_close(self):
        print('WebSocket closed')
