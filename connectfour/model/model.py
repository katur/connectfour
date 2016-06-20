from connectfour.config import (ConnectFourColor, TryAgainReason,
                                DEFAULT_ROWS, DEFAULT_COLUMNS, DEFAULT_TO_WIN)
from connectfour.model.board import ConnectFourBoard
from connectfour.model.player import ConnectFourPlayer
from connectfour.pubsub import Action, publish


class ConnectFourModel(object):
    """Top-level model for the Connect Four game.

    Dependencies between the Core methods:

    -   create_board() and add_player() must both be called at least
        once before calling start_round().

    -   add_player() should be called multiple times to add multiple
        players.

    -   If create_board() is called more than once, the old board is
        replaced with the new board.

    -   After calling start_round() the first time, a gaming session
        has begun, and neither create_board() or add_player() can be
        called again.

    -   start_round() can only be called again after a win or draw is
        announced.

    -   play_disc() can only be called while a round is in progress.
    """

    def __init__(self):
        """Create this model."""
        self.board = None
        self.players = []
        self.used_colors = set()

        self.session_in_progress = False
        self.round_in_progress = False
        self.round_number = 0

        # Which player goes first in the next round
        self.first_turn_index = 0

        # Which player goes next in the current round
        self.current_player_index = 0

    def __str__(self):
        return 'ConnectFourModel [board:{}, num_players:{}]'.format(
            self.board, self.get_num_players())

    def __repr__(self):
        return self.__str__()

    ################
    # Core methods #
    ################

    def create_board(self, num_rows=DEFAULT_ROWS, num_columns=DEFAULT_COLUMNS,
                     num_to_win=DEFAULT_TO_WIN):
        """Create a playing board and add it to the model.

        Publishes a board_created Action.

        This function is separate from __init__ so that players can be
        added before finalizing the board dimensions.

        Args:
            num_rows (Optional[int]): Number of rows in the board.
                Must be at least 1. Default defined in connectfour.config.
            num_columns (Optional[int]): Number of columns in the board.
                Must be at least 1. Default defined in connectfour.config.
            num_to_win (Optional[int]): Number of discs in a row to win.
                Must be at least 1. Default defined in connectfour.config.
        Raises:
            RuntimeError: If gaming session has already started.
            ValueError: If either dimension or the num_to_win is less than 1.
        """
        if self.session_in_progress:
            raise RuntimeError('Cannot add board once session is started')

        if num_rows < 1 or num_columns < 1 or num_to_win < 1:
            raise ValueError('Board dimensions and num_to_win must be >= 1')

        self.board = ConnectFourBoard(num_rows, num_columns, num_to_win)
        publish(Action.board_created, self.board)

    def add_player(self, name, color):
        """Add a player.

        Publishes a player_added Action.

        Args:
            name (str): The player's name. Must be non-empty. Does not need
                to be unique (two Emilys are distinguishable by disc color).
            color (ConnectFourColor): Color of this player's discs. Must be
                unique.
        Raises:
            RuntimeError: If gaming session has already started.
            ValueError: If name is empty or if color is already in use by
                another player.
        """
        if self.session_in_progress:
            raise RuntimeError('Cannot add player once session is started')

        if not name:
            raise ValueError('Name is required and must be non-empty')

        if color in self.used_colors:
            raise ValueError('Color {} is already used'.format(color))

        self.used_colors.add(color)
        player = ConnectFourPlayer(name, color)
        self.players.append(player)
        publish(Action.player_added, player)

    def start_round(self):
        """Start a new round of the game.

        Publishes a round_started Action, followed by a next_player Action
        to indicate which player should go first.

        Raises:
            RuntimeError: If another round is already in progress, if
                there is no board, or if there are no players.
        """
        if self.round_in_progress:
            raise RuntimeError('Cannot start a round with another in progress')

        if not self.board:
            raise RuntimeError('Cannot start a round with no board')

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

        The disc is assumed to be played by the current player.

        If the play is illegal, publishes a try_again Action.
        Otherwise, publishes a disc_played Action, followed by one of
        the following Actions (depending on the outcome of the play);
        round_won, round_draw, or next_player.

        Args:
            column (int): The column to play the disc in.
        Raises:
            RuntimeError: If a round is not currently in progress.
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
        player.num_wins += 1
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
        """Get the number of rows in the board.

        Returns:
            int: The number of rows, or None if there is no board.
        """
        if not self.board:
            return None

        return self.board.num_rows

    def get_num_columns(self):
        """Get the number of columns in the board.

        Returns:
            int: The number of columns, or None if there is no board.
        """
        if not self.board:
            return None

        return self.board.num_columns

    def get_num_to_win(self):
        """Get the number needed to win.

        Returns:
            int: The number to win, or None if there is no board.
        """
        if not self.board:
            return None

        return self.board.num_to_win

    def get_num_players(self):
        """Get the total number of players.

        Returns:
            int: The number of players.
        """
        return len(self.players)

    def get_current_player(self):
        """Get the current player.

        Returns:
            ConnectFourPlayer: Current player, or None if no players added.
        """
        if not self.players:
            return None

        return self.players[self.current_player_index]

    def get_remaining_colors(self):
        """Get the colors that have not been used yet.

        Returns:
            set: A set of unused ConnectFourColors, or the empty set if all
                colors are in use.
        """
        return set(ConnectFourColor) - self.used_colors
