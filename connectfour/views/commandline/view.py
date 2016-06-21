import sys

from connectfour.config import COLORS
from connectfour.pubsub import Action, subscribe


class CommandLineView(object):
    """Simple view that simply logs when actions occur."""

    def __init__(self, model, stream=sys.stdout):
        self.stream = stream
        self.model = model
        self._create_subscriptions()
        self._prompt_create_board()
        self._prompt_add_players()
        self.model.start_round()

    def _create_subscriptions(self):
        responses = {
            Action.player_added: self.on_player_added,
            Action.board_created: self.on_board_created,
            Action.round_started: self.on_round_started,
            Action.next_player: self.on_next_player,
            Action.try_again: self.on_try_again,
            Action.disc_played: self.on_disc_played,
            Action.round_won: self.on_round_won,
            Action.round_draw: self.on_round_draw,
        }

        for action, response in responses.iteritems():
            subscribe(action, response)

    def on_board_created(self, board):
        self.stream.write('Board created: {}\n'.format(board))

    def on_player_added(self, player):
        self.stream.write('Welcome, {}!\n'.format(player))

    def on_round_started(self, round_number):
        self.stream.write('Round started: {}\n'.format(round_number))

    def on_next_player(self, player):
        self._prompt_play_disc(player)

    def on_try_again(self, player, reason):
        self.stream.write('Illegal move: {}\n'.format(reason))
        self._prompt_play_disc(player)

    def on_disc_played(self, player, position):
        self._print_grid()

    def on_round_won(self, player, winning_positions):
        self.stream.write('Round won by: {}, winning discs: {}\n'
                          .format(player, winning_positions))
        self._prompt_play_again()

    def on_round_draw(self):
        self.stream.write('Round ended in a draw.\n')
        self._prompt_play_again()

    def _prompt_create_board(self):
        num_rows = int(raw_input('Num rows: '))
        num_columns = int(raw_input('Num cols: '))
        num_to_win = int(raw_input('Num to win: '))
        self.model.create_board(num_rows, num_columns, num_to_win)

    def _prompt_add_players(self):
        while True:
            name = raw_input('Player name: ')
            index = self.model.get_num_players()
            self.model.add_player(name, COLORS[index])
            response = raw_input('Add another player? [Y/n]: ')
            if response != 'Y':
                break

    def _prompt_play_disc(self, player):
        column = int(raw_input('Where would you like to play, {}? '
                               .format(player)))
        self.model.play_disc(column)

    def _prompt_play_again(self):
        response = raw_input('Play again? [Y/n]: ')
        if response == 'Y':
            self.model.start_round()

    def _print_grid(self):
        max_color_len = max(len(color.name) for color in COLORS)
        width = max_color_len + 1
        grid = self.model.board.get_printable_grid(field_width=width)
        self.stream.write(grid)
