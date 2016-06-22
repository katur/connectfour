import sys

from connectfour.model import (DEFAULT_ROWS, DEFAULT_COLUMNS, DEFAULT_TO_WIN,
                               Color)
from connectfour.pubsub import Action, subscribe
from connectfour.views.util import get_positive_int, get_nonempty_string

MAX_NAME_LENGTH = 50
MAX_ROWS = 100
MAX_COLUMNS = 100
MAX_TO_WIN = 100

YES_RESPONSES = ['y', 'Y']


class CommandLineView(object):
    """View to play Connect Four from the command line."""

    def __init__(self, model):
        """Create this view.

        Args:
            model (ConnectFourModel): The model this view interacts with.
        """
        self.out = sys.stdout
        self.model = model
        self._create_subscriptions()

        self.prompt_create_board()
        self.prompt_add_players()
        self.model.start_game()

    def _create_subscriptions(self):
        responses = {
            Action.player_added: self.on_player_added,
            Action.board_created: self.on_board_created,
            Action.game_started: self.on_game_started,
            Action.next_player: self.on_next_player,
            Action.try_again: self.on_try_again,
            Action.color_played: self.on_color_played,
            Action.game_won: self.on_game_won,
            Action.game_draw: self.on_game_draw,
        }

        for action, response in responses.iteritems():
            subscribe(action, response)

    ##################
    # Call the model #
    ##################

    def prompt_create_board(self):
        num_rows = self._prompt_until_valid(
            'Num rows ({} if blank): '.format(DEFAULT_ROWS),
            get_positive_int, name='Rows', max_value=MAX_ROWS,
            default_if_blank=DEFAULT_ROWS)
        num_columns = self._prompt_until_valid(
            'Num columns ({} if blank): '.format(DEFAULT_COLUMNS),
            get_positive_int, name='Columns', max_value=MAX_COLUMNS,
            default_if_blank=DEFAULT_COLUMNS)
        num_to_win = self._prompt_until_valid(
            'Num to win ({} if blank): '.format(DEFAULT_TO_WIN),
            get_positive_int, name='To Win', max_value=MAX_TO_WIN,
            default_if_blank=DEFAULT_TO_WIN)

        self.model.create_board(num_rows, num_columns, num_to_win)

    def prompt_add_players(self):
        while True:
            name = self._prompt_until_valid(
                'Player name: ', get_nonempty_string, name='Name', max_len=50)
            index = self.model.get_num_players()
            self.model.add_player(name.strip(), Color(index))
            response = raw_input('Add another player? [y/n]: ')

            if response.strip() not in YES_RESPONSES:
                return

    def prompt_play(self, player):
        column = int(raw_input('Where would you like to play, {}? '
                               .format(player)))
        self.model.play(column)

    def prompt_play_again(self):
        response = raw_input('Play again? [y/n]: ')
        if response.strip() in YES_RESPONSES:
            self.model.start_game()

    def _prompt_until_valid(self, prompt, condition, **kwargs):
        while True:
            try:
                return condition(raw_input(prompt), **kwargs)
            except ValueError as e:
                self.out.write('Try again: {}\n'.format(e))

    ###########################
    # Respond to model events #
    ###########################

    def on_board_created(self, board):
        self.out.write('Board created: {}\n\n'.format(board))

    def on_player_added(self, player):
        self.out.write('Welcome, {}!\n\n'.format(player))

    def on_game_started(self, game_number):
        self.out.write('Game {} started\n'.format(game_number))
        self._print_grid()

    def on_next_player(self, player):
        self.prompt_play(player)

    def on_try_again(self, player, reason):
        self.out.write('Illegal move: {}\n'.format(reason))
        self.prompt_play(player)

    def on_color_played(self, color, position):
        self._print_grid()

    def on_game_won(self, player, winning_positions):
        self.out.write('Game won by: {}. Winning positions:\n'.format(player))
        self._print_grid(limit_positions=winning_positions)
        self.prompt_play_again()

    def on_game_draw(self):
        self.out.write('Game ended in a draw.\n\n')
        self.prompt_play_again()

    def _print_grid(self, **kwargs):
        grid = self.model.get_printable_grid(show_columns=True, **kwargs)
        self.out.write('\n' + grid + '\n')
