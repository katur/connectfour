import sys

from connectfour.pubsub import ModelAction


class LogView(object):
    """View that simply logs when Connect Four events occur.

    Args:
        out (Optional): Where to write output to. Defaults to stdout.
            Can be any object with a `write` method.
    """

    def __init__(self, pubsub, out=sys.stdout):
        self.pubsub = pubsub
        self.out = out
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

        for action, response in responses.items():
            self.pubsub.subscribe(action, response)

    def on_board_created(self, board):
        self.out.write('Board created: {}\n'.format(board))

    def on_player_added(self, player):
        self.out.write('Player added: {}\n'.format(player))

    def on_game_started(self):
        self.out.write('Game started\n')

    def on_next_player(self, player):
        self.out.write('Next turn: {}\n'.format(player))

    def on_try_again(self, player, reason):
        self.out.write('Try again: {}\n'.format(player, reason))

    def on_color_played(self, color, position):
        self.out.write('{} played in position: {}\n'
                       .format(color.name, position))

    def on_game_won(self, player, winning_positions):
        self.out.write('Game won by: {}, winning positions: {}\n'
                       .format(player, winning_positions))

    def on_game_draw(self):
        self.out.write('Game ended in a draw.\n')
