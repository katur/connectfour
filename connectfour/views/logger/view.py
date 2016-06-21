import sys

from connectfour.pubsub import Action, subscribe


class LogView(object):
    """View that simply logs when Connect Four events occur.

    Args:
        out (Optional): Where to write output to. Defaults to stdout.
            Can be any object with a `write` method.
    """

    def __init__(self, out=sys.stdout):
        self.out = out
        self._create_subscriptions()

    def _create_subscriptions(self):
        responses = {
            Action.player_added: self.on_player_added,
            Action.board_created: self.on_board_created,
            Action.game_started: self.on_game_started,
            Action.next_player: self.on_next_player,
            Action.try_again: self.on_try_again,
            Action.disc_played: self.on_disc_played,
            Action.game_won: self.on_game_won,
            Action.game_draw: self.on_game_draw,
        }

        for action, response in responses.iteritems():
            subscribe(action, response)

    def on_player_added(self, player):
        self.out.write('Player added: {}\n'.format(player))

    def on_board_created(self, board):
        self.out.write('Board created: {}\n'.format(board))

    def on_game_started(self, game_number):
        self.out.write('Game {} started\n'.format(game_number))

    def on_next_player(self, player):
        self.out.write('Next turn: {}\n'.format(player))

    def on_try_again(self, player, reason):
        self.out.write('Try again: {}\n'.format(player, reason))

    def on_disc_played(self, player, position):
        self.out.write('Disc played by: {}, position: {}\n'
                       .format(player, position))

    def on_game_won(self, player, winning_positions):
        self.out.write('Game won by: {}, winning positions: {}\n'
                       .format(player, winning_positions))

    def on_game_draw(self):
        self.out.write('Game ended in a draw.\n')
