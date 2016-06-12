import sys

from connectfour import pubsub


class LogView(object):
    def __init__(self, game, stream=sys.stdout):
        self.stream = stream
        self.game = game
        self._create_subscriptions()

    def _create_subscriptions(self):
        responses = {
            pubsub.Action.player_added: self._on_player_added,
            pubsub.Action.round_started: self._on_round_started,
            pubsub.Action.next_player: self._on_next_player,
            pubsub.Action.try_again: self._on_try_again,
            pubsub.Action.disc_played: self._on_disc_played,
            pubsub.Action.round_won: self._on_round_won,
            pubsub.Action.round_draw: self._on_round_draw,
        }
        for action, response in responses.iteritems():
            pubsub.subscribe(action, response)

    def _on_player_added(self, player):
        self.stream.write('Player added: {}\n'.format(player))

    def _on_round_started(self, round_number):
        self.stream.write('Round started: {}\n'.format(round_number))

    def _on_next_player(self, player):
        self.stream.write('Next turn: {}\n'.format(player))

    def _on_try_again(self, player, reason):
        self.stream.write('Try again: {}\n'.format(player, reason))

    def _on_disc_played(self, player, position):
        self.stream.write('Disc played by: {}, position: {}\n'
                          .format(player, position))

    def _on_round_won(self, player, winning_positions):
        self.stream.write('Round won by: {}, winning discs: {}\n'
                          .format(player, winning_positions))

    def _on_round_draw(self):
        self.stream.write('Round ended in a draw.\n')
