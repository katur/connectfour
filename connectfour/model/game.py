from connectfour.pubsub import publish, Action
from connectfour.config import Color
from connectfour.config import TryAgainReason
from connectfour.model.board import Board
from connectfour.model.player import Player

# TODO: these defaults should maybe be in higher class for use by view
DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7
DEFAULT_TO_WIN = 4


class Game(object):
    """Top-level model of the Connect Four game."""

    def __init__(self):
        self.board = None
        self.players = []
        self.used_colors = set()
        self.used_names = set()

        self.session_in_progress = False
        self.round_in_progress = False
        self.round_number = 0

        # Which player goes first in the next round
        self.first_turn_index = 0

        # Which player goes next in the current round
        self.current_player_index = 0

    def __str__(self):
        return 'Game [board:{}, num_players:{}]'.format(
            self.board, self.get_num_players())

    def __repr__(self):
        return self.__str__()

    ######################
    # Game setup methods #
    ######################

    def add_board(self, num_rows=DEFAULT_ROWS, num_columns=DEFAULT_COLUMNS,
                  num_to_win=DEFAULT_TO_WIN):
        """Create a playing board and add to the game.

        This is not done in __init__ so that players can be added prior to
        choosing the board dimensions.
        """
        # TODO: these checks should maybe be in Board class?
        if num_rows < 1 or num_columns < 1 or num_to_win < 1:
            raise ValueError('Board rows, columns, and num_to_win '
                             'must be at least 1')

        # TODO: maybe nix this check (no reason game can't proceed even
        # if a draw is inevitable)
        if num_to_win > num_rows and num_to_win > num_columns:
            raise ValueError('Number to win must be at least 1, and '
                             'cannot exceed both the number of rows '
                             'and the number of columns')

        self.board = Board(num_rows, num_columns, num_to_win)

    def add_player(self, name, color):
        """Add a player to the session."""
        # TODO: this check may be unnecessary (just document)
        # If do check for this, should also make sure game hasn't begun
        if self.session_in_progress:
            raise RuntimeError('Cannot add player before session started')

        # TODO: this check redundant with below, but should handle in view
        if len(self.used_colors) >= len(Color):
            raise RuntimeError('Game has reached max players')

        if color in self.used_colors:
            raise ValueError('Color {} is already used'.format(color))

        # TODO: empty/unique string enforcement maybe just limit to view
        if not name:
            raise ValueError('Name is required and must be non-empty')

        if name in self.used_names:
            raise ValueError('Name {} is already used')

        self.used_colors.add(color)
        self.used_names.add(name)
        player = Player(name, color)
        self.players.append(player)
        publish(Action.player_added, player)

    #####################
    # Game play methods #
    #####################

    def start_round(self):
        """Start a new round of the game."""
        if self.round_in_progress:
            raise RuntimeError('Cannot start a round while another '
                               'is in progress')
        if not self.players:
            raise RuntimeError('Cannot start a round with no players')

        self.board.reset()
        self.session_in_progress = True
        self.round_in_progress = True
        self.round_number += 1
        publish(Action.round_started, self.round_number)

        self.current_player_index = self.first_turn_index

        # Prep first_turn_index for the next round
        self.first_turn_index = ((self.first_turn_index + 1)
                                 % self.get_num_players())

        publish(Action.next_player, self.get_current_player())

    def play_disc(self, column):
        """Play a disc in a column.

        Assumes the disc is played by the current player.

        Cannot play a disc before a round is started.
        """
        if not self.round_in_progress:
            raise RuntimeError('Cannot play disc before round has started')

        if not self.board.is_column_in_bounds(column):
            publish(Action.try_again, self.get_current_player(),
                    TryAgainReason.column_out_of_bounds)

        elif self.board.is_column_full(column):
            publish(Action.try_again, self.get_current_player(),
                    TryAgainReason.column_full)

        else:
            self._process_play(column)

    ##########################
    # Helpers to play_disc() #
    ##########################

    def _process_play(self, column):
        player = self.get_current_player()
        row = self.board.add_disc(player.disc, column)
        publish(Action.disc_played, player, (row, column))

        winning_positions = self.board.get_winning_positions((row, column))

        if winning_positions:
            self._process_win(player, winning_positions)
        elif self.board.is_full():
            self._process_draw()
        else:
            self._process_next_player()

    def _process_win(self, player, winning_positions):
        self.round_in_progress = False
        player.number_of_wins += 1
        publish(Action.round_won, player, winning_positions)

    def _process_draw(self):
        self.round_in_progress = False
        publish(Action.round_draw)

    def _process_next_player(self):
        self.current_player_index = ((self.current_player_index + 1)
                                     % self.get_num_players())

        publish(Action.next_player, self.get_current_player())

    ##################
    # Simple getters #
    ##################

    def get_num_rows(self):
        return self.board.num_rows

    def get_num_columns(self):
        return self.board.num_columns

    def get_current_player(self):
        if not self.players:
            raise RuntimeError('Cannot get current player if no '
                               'players have been added yet')
        return self.players[self.current_player_index]

    def get_player(self, index):
        if index < 0 or index >= self.get_num_players():
            raise IndexError('Player index {} is out of bounds'.format(index))
        return self.players[index]

    def get_num_players(self):
        return len(self.players)

    def get_remaining_colors(self):
        return set(Color) - self.used_colors
