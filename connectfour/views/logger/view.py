import sys

from connectfour import pubsub


class LogView(object):
    def __init__(self, game, stream=sys.stdout):
        self.stream = stream
        self.game = game
        self._create_subscriptions()

    def _create_subscriptions(self):
        responses = {
            pubsub.Action.player_added: self.on_player_added,
            pubsub.Action.round_started: self.on_round_started,
            pubsub.Action.next_player: self.on_next_player,
            pubsub.Action.try_again: self.on_try_again,
            pubsub.Action.disc_played: self.on_disc_played,
            pubsub.Action.round_won: self.on_round_won,
            pubsub.Action.round_draw: self.on_round_draw,
        }
        for action, response in responses.iteritems():
            pubsub.subscribe(action, response)

    def on_player_added(self, player):
        self.stream.write('Player added: {}\n'.format(player))

    def on_round_started(self, round_number):
        self.stream.write('Round started: {}\n'.format(round_number))

    def on_next_player(self, player):
        self.stream.write('Next turn: {}\n'.format(player))

    def on_try_again(self, player, reason):
        self.stream.write('Try again: {}\n'.format(player, reason))

    def on_disc_played(self, player, position):
        self.stream.write('Disc played by: {}, position: {}\n'
                          .format(player, position))

    def on_round_won(self, player, winning_positions):
        self.stream.write('Round won by: {}, winning discs: {}\n'
                          .format(player, winning_positions))

    def on_round_draw(self):
        self.stream.write('Round ended in a draw.\n')