import operator
from connectfour.config import (DEFAULT_ROWS, DEFAULT_COLUMNS, DEFAULT_TO_WIN,
                                Color, TryAgainReason)
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

        self.board = Board(num_rows, num_columns, num_to_win)
        publish(Action.board_created, self.board)

    def add_player(self, name, color):
        """Add a player.

        Publishes a player_added Action.

        Args:
            name (str): The player's name. Must be non-empty. Does not need
                to be unique (two Emilys are distinguishable by disc color).
            color (Color): Color of this player's discs. Must be unique.
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
        player = Player(name, color)
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

    ###########################
    # Helpers for play_disc() #
    ###########################

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
    # Simple helpers #
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
            Player: Current player, or None if no players added.
        """
        if not self.players:
            return None

        return self.players[self.current_player_index]

    def get_remaining_colors(self):
        """Get the colors that have not been used yet.

        Returns:
            set: A set of unused Colors, or the empty set if all colors are
                in use.
        """
        return set(Color) - self.used_colors


class Player(object):
    """A Connect Four player."""

    def __init__(self, name, color):
        """Create a player.

        Args:
            name (str): This player's name.
            color (Color): The color of this player's discs.
        """
        self.name = name
        self.disc = Disc(color)
        self.num_wins = 0

    def __str__(self):
        return '{} ({})'.format(self.name, self.disc.color.name)

    def __repr__(self):
        return self.__str__()

    def get_color(self):
        """Get this player's disc color.

        Returns:
            Color: The color of this player's discs.
        """
        return self.disc.color


class Disc(object):
    """A Connect Four playing disc (aka token, or chip).

    Two discs are considered equal if they are the same color.
    """

    def __init__(self, color):
        """Create a disc.

        Args:
            color (Color): This disc's color.
        """
        self.color = color

    def __str__(self):
        return '{}'.format(self.color.name)

    def __repr__(self):
        return '{} Disc'.format(self.color)

    def __eq__(self, other):
        return type(other) is type(self) and self.color == other.color

    def __ne__(self, other):
        return not self.__eq__(other)


class Board(object):
    """A Connect Four playing board."""

    def __init__(self, num_rows, num_columns, num_to_win):
        """Create a board.

        Args:
            num_rows (int): The number of rows in this board's grid.
            num_columns (int): The number of columns in this board's grid.
            num_to_win (int): The number of adjacent discs needed to win.
        """
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_to_win = num_to_win

        self.top_row = 0
        self.bottom_row = num_rows - 1
        self.left_column = 0
        self.right_column = num_columns - 1

        self.grid = [[None for column in range(num_columns)]
                     for row in range(num_rows)]

    def __str__(self):
        return '{} rows x {} columns ({} to win)'.format(
            self.num_rows, self.num_columns, self.num_to_win)

    def __repr__(self):
        return self.__str__()

    def get_printable_grid(self, field_width=8):
        """Get a "pretty" string of this board's grid.

        Might be used for console printing.

        Args:
            field_width (Optional[int]): The number of spaces each disc
                should take up. Defaults to 8 characters

        Returns:
            str: A formatted string of the grid.
        """
        output = ''
        for i in range(self.num_columns):
            output += '{0:<{width}}'.format(i, width=field_width)
        output += '\n'

        for row in self.grid:
            for column in row:
                el = column if column else '-'
                output += '{0:{width}}'.format(el, width=field_width)
            output += '\n'

        return output

    def reset(self):
        """Reset this board for a new game.

        Sets all positions in this board's grid to None.
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                self.grid[row][column] = None

    def add_disc(self, disc, column):
        """Add a disc to a column.

        Args:
            disc (Disc): The disc to add.
            column (int): The column to add the disc to.
        Returns:
            int: The row in which the disc landed.
        Raises:
            ValueError: If column is full or out of bounds.
        """
        if not self.is_column_in_bounds(column):
            raise ValueError('Column {} out of bounds'.format(column))

        if self.is_column_full(column):
            raise ValueError('Column {} is full'.format(column))

        current_row = self.bottom_row

        while self.get_disc((current_row, column)) is not None:
            current_row -= 1

        self.grid[current_row][column] = disc
        return current_row

    def get_winning_positions(self, origin, fake_disc=None):
        """Get winning positions that include some origin position.

        Args:
            origin: A 2-tuple (row, column) that will be part of any
                wins found.
            fake_disc (Optional[Disc]): A disc to pretend is
                at start. Might be used to predict whether a win might
                occur without actually playing the disc.
        Returns:
            set: A set of 2-tuples in format (row, column) of the positions
                that result in a win, or the empty set if no win found.
        """
        HORIZONTAL = (0, 1)
        VERTICAL = (1, 0)
        UP_RIGHT = (1, 1)
        DOWN_RIGHT = (1, -1)

        winning_positions = set()

        for step in (HORIZONTAL, VERTICAL, UP_RIGHT, DOWN_RIGHT):
            matches = self._get_consecutive_matches_mirrored(
                origin, step, fake_disc=fake_disc)

            # Check if these matches are enough to win
            if len(matches) >= self.num_to_win:
                winning_positions |= matches

        return winning_positions

    #######################################
    # Helpers for get_winning_positions() #
    #######################################

    def _get_consecutive_matches_mirrored(self, start, step, fake_disc=None):
        """Get consecutive matches in two directions.

        From a starting position, find positions with discs matching the
        starting position, outward in the direction indicated by step
        as well as in the 180-flipped direction, until a mismatch is found.

        Args:
            start: A 2-tuple (row, column) of the starting position.
            step: A 2-tuple (vertical_step, horizontal_step), indicating
                the direction to move with each step. The 180-degree
                rotation of this step will be included as well.

                For example, to check the horizontal axis, step can be
                either (0, 1) or (0, -1).

            fake_disc (Optional[Disc]): See docstring for
                get_winning_positions.
        Returns:
            set: A set of 2-tuples in format (row, column) of the matching
                positions, including the starting position.
        """
        flipped_step = tuple(-i for i in step)

        a = self._get_consecutive_matches(start, step, fake_disc=fake_disc)
        b = self._get_consecutive_matches(start, flipped_step,
                                          fake_disc=fake_disc)

        return a | b

    def _get_consecutive_matches(self, start, step, fake_disc=None):
        """Get consecutive matches in a single direction.

        From a starting position, find positions with discs matching the
        starting position, outward in the direction indicated by step,
        until a mismatch is found.

        Args:
            start: A 2-tuple (row, column) of the starting position.
            step: A 2-tuple (vertical_step, horizontal_step) indicating
                the direction to move with each step.

                For example, to check straight up, step should be (1, 0).
                To check diagonally down-left, step should be (-1, -1).

            fake_disc (Optional[Disc]): See docstring for
                get_winning_positions.
        Returns:
            set: A set of 2-tuples in format (row, column) of the matching
                positions, including the starting position.
        """
        disc = fake_disc if fake_disc else self.get_disc(start)

        # Initialize set with start position
        positions = {start}

        current = tuple(map(operator.add, start, step))

        while (self.is_in_bounds(current) and self.get_disc(current) == disc):
            positions.add(current)
            current = tuple(map(operator.add, current, step))

        return positions

    ##################
    # Simple helpers #
    ##################

    def get_disc(self, position):
        """Retrieve a disc from this board.

        Args:
            position: A 2-tuple in format (row, column).
        Returns:
            Disc: The disc at this position, or None if this
                position is empty.
        Raises:
            ValueError: If position is out of bounds.
        """
        if not self.is_in_bounds(position):
            raise ValueError('Position {} is out of bounds'
                             .format(position))

        row, column = position
        return self.grid[row][column]

    def is_row_in_bounds(self, row):
        """Determine if a row is in bounds.

        Args:
            row (int): The row to check.
        Returns:
            bool: True if in bounds, False otherwise.
        """
        return row >= self.top_row and row <= self.bottom_row

    def is_column_in_bounds(self, column):
        """Determine if a column is in bounds.

        Args:
            column (int): The column to check.
        Returns:
            bool: True if in bounds, False otherwise.
        """
        return column >= self.left_column and column <= self.right_column

    def is_in_bounds(self, position):
        """Determine if position is in bounds.

        Args:
            position: A 2-tuple in format (row, column).
        Returns:
            bool: True if in bounds, False otherwise.
        """
        row, column = position
        return self.is_row_in_bounds(row) and self.is_column_in_bounds(column)

    def is_column_full(self, column):
        """Determine if a column is full of discs.

        Args:
            column (int): The column to check.
        Returns:
            bool: True if column is full, False otherwise.
        Raises:
            ValueError: If column is out of bounds.
        """
        if not self.is_column_in_bounds(column):
            raise ValueError('Column {} is out of bounds'.format(column))

        return self.grid[self.top_row][column] is not None

    def is_full(self):
        """Determine if this board is entirely full of discs.

        Returns:
            bool: True if this board is full, False otherwise.
        """
        for i in range(self.num_columns):
            if not self.is_column_full(i):
                return False

        return True
