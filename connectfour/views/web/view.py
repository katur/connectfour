import tornado.web
import tornado.websocket

from connectfour import pubsub
from connectfour.model import ConnectFourModel, Color
from connectfour.pubsub import ModelAction, ViewAction, publish, subscribe


def make_model():
    model = ConnectFourModel()
    model._create_board(6, 7, 5)
    model._add_player('Jim', Color.black)
    model._add_player('Sally', Color.red)
    model._start_game()
    return model


class SetupHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        super(SetupHandler, self).__init__(*args, **kwargs)

    def get(self):
        self.render('setup.html', title='Setup Page')


class GameHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        super(GameHandler, self).__init__(*args, **kwargs)

    def get(self):
        self.render('game.html', title='Game Page',
                    model=self.model,
                    num_rows=self.model.get_num_rows(),
                    num_columns=self.model.get_num_columns(),
                    num_to_win=self.model.get_num_to_win())


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self._create_subscriptions()
        super(WebSocketHandler, self).__init__(*args, **kwargs)

    def _create_subscriptions(self):
        responses = {
            ModelAction.next_player: self.on_next_player,
            ModelAction.try_again: self.on_try_again,
            ModelAction.color_played: self.on_color_played,
            ModelAction.game_won: self.on_game_won,
            ModelAction.game_draw: self.on_game_draw,
        }

        for action, response in responses.iteritems():
            subscribe(action, response)

    def on_next_player(self, player):
        pass

    def on_try_again(self, player, reason):
        pass

    def on_color_played(self, color, position):
        pass

    def on_game_won(self, player, winning_positions):
        pass

    def on_game_draw(self):
        pass

    def on_message(self, message):
        """Handle incoming messages."""
        print 'Received message: {}'.format(message)
        if message.isdigit():
            column = int(message)
            self.write_message('Requesting play in column {}'
                               .format(column))
            publish(ViewAction.play, column)
            pubsub.trigger()

    def on_close(self):
        print('WebSocket closed')
