import sys


class LogView(object):
    def __init__(self, game, stream=sys.stdout):
        self.stream = stream
        self.game = game
        game.add_listener(self)

    def player_added(self, player):
        self.stream.write('Player added: {}\n'.format(player))

    def round_started(self, round_number):
        self.stream.write('Round started: {}\n'.format(round_number))

    def next_player(self, player):
        self.stream.write('Next turn: {}\n'.format(player))

    def try_again(self, player, reason):
        self.stream.write('Try again: {}\n'.format(player, reason))

    def disc_played(self, player, position):
        self.stream.write('Disc played by: {}, position: {}\n'
                          .format(player, position))

    def round_won(self, player, winning_positions):
        self.stream.write('Round won by: {}, winning discs: {}\n'
                          .format(player, winning_positions))

    def round_draw(self):
        self.stream.write('Round ended in a draw.\n')
