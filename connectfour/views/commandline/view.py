import sys

from connectfour.model import (DEFAULT_ROWS, DEFAULT_COLUMNS, DEFAULT_TO_WIN,
                               Color, TryAgainReason)
from connectfour.pubsub import Action, subscribe
from connectfour.views.util import (get_positive_int, get_int,
                                    get_stripped_nonempty_string)

MAX_NAME_LENGTH = 50
MAX_ROWS = 100
MAX_COLUMNS = 100
MAX_TO_WIN = 100

YES_RESPONSES = ['y', 'Y']

REASON_TEXT = {
    TryAgainReason.column_out_of_bounds: 'Column out of bounds',
    TryAgainReason.column_full: 'Column full',
}


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

        self._create_board()
        self._add_players()
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
        if player.is_ai:
            self.out.write('AI player {} is playing\n'.format(player))
        else:
            self._play(player)

    def on_try_again(self, player, reason):
        self.out.write('Try again: {}\n'.format(REASON_TEXT[reason]))
        self._play(player)

    def on_color_played(self, color, position):
        self._print_grid()

    def on_game_won(self, player, winning_positions):
        self.out.write('Game won by: {}. Winning positions:\n'.format(player))
        self._print_grid(show_only=winning_positions)
        self._start_new_game()

    def on_game_draw(self):
        self.out.write('Game ended in a draw.\n\n')
        self._start_new_game()

    def _print_grid(self, **kwargs):
        grid = self.model.get_printable_grid(show_labels=True, **kwargs)
        self.out.write('\n' + grid + '\n')

    ##################
    # Call the model #
    ##################

    def _create_board(self):
        num_rows = self._prompt_until_valid(
            prompt='Num rows ({} if blank): '.format(DEFAULT_ROWS),
            condition=get_positive_int, name='Rows', max_value=MAX_ROWS,
            default_if_blank=DEFAULT_ROWS)
        num_columns = self._prompt_until_valid(
            prompt='Num columns ({} if blank): '.format(DEFAULT_COLUMNS),
            condition=get_positive_int, name='Columns', max_value=MAX_COLUMNS,
            default_if_blank=DEFAULT_COLUMNS)
        num_to_win = self._prompt_until_valid(
            prompt='Num to win ({} if blank): '.format(DEFAULT_TO_WIN),
            condition=get_positive_int, name='To Win', max_value=MAX_TO_WIN,
            default_if_blank=DEFAULT_TO_WIN)

        self.model.create_board(num_rows, num_columns, num_to_win)

    def _add_players(self):
        while True:
            name = self._prompt_until_valid(
                prompt='Player name: ', condition=get_stripped_nonempty_string,
                name='Name', max_len=50)
            is_ai = self._prompt_yes_no('Is AI?')
            index = self.model.get_num_players()
            self.model.add_player(name, Color(index), is_ai)
            if not self._prompt_yes_no('Add another player?'):
                return

    def _play(self, player):
        column = self._prompt_until_valid(
            prompt='Where would you like to play, {}? '.format(player),
            condition=get_int, name='Column')
        self.model.play(column)

    def _start_new_game(self):
        if self._prompt_yes_no('Play again?'):
            self.model.start_game()

    def _prompt_until_valid(self, prompt, condition, **kwargs):
        while True:
            try:
                return condition(raw_input(prompt), **kwargs)
            except ValueError as e:
                self.out.write('Try again: {}\n'.format(e))

    def _prompt_yes_no(self, prompt):
        response = raw_input('{} [y/n]: '.format(prompt)).strip()
        return response in YES_RESPONSES
