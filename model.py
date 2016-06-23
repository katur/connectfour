import operator
from enum import Enum

from pubsub import Action, publish

DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7
DEFAULT_TO_WIN = 4


class ConnectFourModel(object):
    """Top-level model for the Connect Four game.

    This model supports numbers other than Four (Connect Three, Six, etc.), as
    well as variable board dimensions and a variable number of players.

    Dependencies between the core methods:

    -   create_board() and add_player() must be called at least once before
        calling start_game(), and cannot be called after calling start_game().

    -   add_player() should be called multiple times to add multiple players.
        Since each player must have a distinct color, the number of players is
        capped at len(Color).

    -   If create_board() is called more than once, the old board is replaced
        with the new board.

    -   start_game() can only be called again after a win or draw is announced.

    -   play() can only be called while a game is in progress.
    """

    def __init__(self):
        """Create this model."""
        self.board = None
        self.players = []
        self.used_colors = set()

        self.session_in_progress = False
        self.game_in_progress = False
        self.game_number = 0

        # Which player goes first in the next game
        self.first_player_index = 0

        # Which player goes next in the current game
        self.current_player_index = 0

    def __repr__(self):
        return 'ConnectFourModel board={}, num_players={}'.format(
            self.board, self.get_num_players())

    def create_board(self, num_rows=DEFAULT_ROWS, num_columns=DEFAULT_COLUMNS,
                     num_to_win=DEFAULT_TO_WIN):
        """Create a playing board and add it to the model.

        Publishes a board_created Action.

        Args:
            num_rows (Optional[int]): Number of rows in the board.
                Must be positive.
            num_columns (Optional[int]): Number of columns in the board.
                Must be positive.
            num_to_win (Optional[int]): Number in a row to win.
                Must be positive.
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
                to be unique (two Emilys are distinguishable by color).
            color (Color): This player's playing color. Must be unique.
        Raises:
            RuntimeError: If gaming session has already started.
            ValueError: If name is empty or if color is already in use.
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

    def start_game(self):
        """Start a new game.

        Publishes a game_started Action, followed by a next_player Action
        to indicate which player should go first.

        Raises:
            RuntimeError: If another game is already in progress, if there is
                no board, or if there are no players.
        """
        if self.game_in_progress:
            raise RuntimeError('Cannot start a game with another in progress')

        if not self.board:
            raise RuntimeError('Cannot start a game with no board')

        if not self.players:
            raise RuntimeError('Cannot start a game with no players')

        self.board.reset()
        self.session_in_progress = True
        self.game_in_progress = True
        self.game_number += 1
        publish(Action.game_started, self.game_number)

        self.current_player_index = self.first_player_index
        self._increment_first_player_index()  # Prep for next game
        publish(Action.next_player, self.get_current_player())

    def play(self, column):
        """Play in a column.

        The play is assumed to be by the current player.

        If the play is illegal, publishes a try_again Action. Otherwise,
        publishes a color_played Action, followed by one of the following
        (depending on the outcome): game_won, game_draw, or next_player.

        Args:
            column (int): The column to play in.
        Raises:
            RuntimeError: If a game is not currently in progress.
        """
        if not self.game_in_progress:
            raise RuntimeError('Cannot play before game has started')

        if not self.board.is_column_in_bounds(column):
            publish(Action.try_again, self.get_current_player(),
                    TryAgainReason.column_out_of_bounds)

        elif self.board.is_column_full(column):
            publish(Action.try_again, self.get_current_player(),
                    TryAgainReason.column_full)

        else:
            self._process_play(column)

    def _process_play(self, column):
        player = self.get_current_player()
        row = self.board.add_color(player.color, column)
        publish(Action.color_played, player.color, (row, column))

        winning_positions = self.board.get_winning_positions((row, column))

        if winning_positions:
            self._process_win(player, winning_positions)
        elif self.board.is_full():
            self._process_draw()
        else:
            self._process_next_player()

    def _process_win(self, player, winning_positions):
        self.game_in_progress = False
        player.num_wins += 1
        publish(Action.game_won, player, winning_positions)

    def _process_draw(self):
        self.game_in_progress = False
        publish(Action.game_draw)

    def _process_next_player(self):
        self._increment_current_player_index()
        publish(Action.next_player, self.get_current_player())

    def _increment_current_player_index(self):
        self.current_player_index = ((self.current_player_index + 1)
                                     % self.get_num_players())

    def _increment_first_player_index(self):
        self.first_player_index = ((self.first_player_index + 1)
                                   % self.get_num_players())

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

    def get_player(self, index):
        """Get the player at a particular playing index.

        Returns:
            Player: The player at index, or None if no player at that index.
        """
        if index >= self.get_num_players():
            return None

        return self.players[index]

    def get_current_player(self):
        """Get the current player.

        Returns:
            Player: Current player, or None if no players added.
        """
        if not self.players:
            return None

        return self.get_player(self.current_player_index)

    def get_printable_grid(self, **kwargs):
        """Get a printable grid of the board.

        Returns:
            str: Formatted string of the board.
        """
        return self.board.get_printable_grid(**kwargs)


class Color(Enum):
    """A color for a player to play in the board."""

    # Yellow omitted to serve as background color (as in the classic game).
    (black, red, blue, purple, brown, green, pink, gray, orange,
        lime) = range(10)


class TryAgainReason(Enum):
    """Reason that a player needs to try again."""

    column_out_of_bounds, column_full = range(2)


class Player(object):
    """A Connect Four player."""

    def __init__(self, name, color):
        """Create a player.

        Args:
            name (str): This player's name.
            color (Color): This player's playing color.
        """
        self.name = name
        self.color = color
        self.num_wins = 0

    def __repr__(self):
        return '{} name={} color={}'.format(
            self.__class__.__name__, self.name, self.color)

    def __str__(self):
        return '{} ({})'.format(self.name, self.color.name)


class Board(object):
    """A Connect Four playing board."""

    def __init__(self, num_rows, num_columns, num_to_win):
        """Create a board.

        Args:
            num_rows (int): Number of rows in this board's grid.
            num_columns (int): Number of columns in this board's grid.
            num_to_win (int): Number in a row needed to win.
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

    def __repr__(self):
        return '{} num_rows={} num_columns={} num_to_win={}'.format(
            self.__class__.__name__, self.num_rows, self.num_columns,
            self.num_to_win)

    def __str__(self):
        return '{} rows x {} columns ({} to win)'.format(
            self.num_rows, self.num_columns, self.num_to_win)

    def reset(self):
        """Reset this board for a new game.

        Sets all positions in this board's grid to None.
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                self.grid[row][column] = None

    def add_color(self, color, column):
        """Add a color to a column.

        Args:
            color (Color): The color to add.
            column (int): The column to add the color to.
        Returns:
            int: The row in which the color landed.
        Raises:
            ValueError: If column is full or out of bounds.
        """
        if not self.is_column_in_bounds(column):
            raise ValueError('Column {} out of bounds'.format(column))

        if self.is_column_full(column):
            raise ValueError('Column {} is full'.format(column))

        current_row = self.bottom_row

        while self.get_color((current_row, column)) is not None:
            current_row -= 1

        self.grid[current_row][column] = color
        return current_row

    def get_winning_positions(self, origin, fake_color=None):
        """Get winning positions that include some origin position.

        Args:
            origin: A 2-tuple (row, column) that will be part of any
                wins found.
            fake_color (Optional[Color]): A color to pretend is
                at start. Might be used to predict whether a win might
                occur without actually playing the color.
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
            matches = self._get_matches_mirrored(
                origin, step, fake_color=fake_color)

            # Check if these matches are enough to win
            if len(matches) >= self.num_to_win:
                winning_positions |= matches

        return winning_positions

    def _get_matches_mirrored(self, start, step, **kwargs):
        """
        From start position, find positions with matching color outward in the
        direction indicated by step as well as in the 180-flipped direction.
        Returns a set of the matching positions, including start.
        """
        flipped_step = tuple(-i for i in step)

        a = self._get_matches(start, step, **kwargs)
        b = self._get_matches(start, flipped_step, **kwargs)

        return a | b

    def _get_matches(self, start, step, fake_color=None):
        """
        From start position, find positions with matching color outward in the
        direction indicated by step. Returns a set of the matching positions,
        including start.
        """
        color = fake_color if fake_color else self.get_color(start)

        # Initialize set with start position
        positions = {start}

        current = tuple(map(operator.add, start, step))

        while (self.is_in_bounds(current) and
                self.get_color(current) == color):
            positions.add(current)
            current = tuple(map(operator.add, current, step))

        return positions

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
        """Determine if a column is full.

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
        """Determine if this board is entirely full.

        Returns:
            bool: True if this board is full, False otherwise.
        """
        for i in range(self.num_columns):
            if not self.is_column_full(i):
                return False

        return True

    def get_color(self, position):
        """Retrieve the color at a position in this board.

        Args:
            position: A 2-tuple in format (row, column).
        Returns:
            Color: The color at this position, or None if empty.
        Raises:
            ValueError: If position is out of bounds.
        """
        if not self.is_in_bounds(position):
            raise ValueError('Position {} is out of bounds'
                             .format(position))

        row, column = position
        return self.grid[row][column]

    def get_printable_grid(self, width=None, show_labels=False,
                           show_only=None):
        """Get a "pretty" string of this board's grid.

        Args:
            width (Optional[int]): Number of characters for each grid position.
            show_labels (Optional[bool]): Whether to show column numbers.
            show_only (Optional[set]): Show colors only in these positions.

        Returns:
            str: A formatted string of the grid.
        """

        if not width:
            width = max(len(color.name) for color in Color) + 2

        output = ''

        if show_labels:
            for i in range(self.num_columns):
                output += '{0:<{width}}'.format(i, width=width)

            output += '\n'

        for row in range(self.num_rows):
            for column in range(self.num_columns):
                position = (row, column)
                color = self.get_color(position)

                if color and (not show_only or position in show_only):
                    s = color.name
                else:
                    s = '-'

                output += '{0:{width}}'.format(s, width=width)

            output += '\n'

        return output
