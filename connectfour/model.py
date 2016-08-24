import operator
import random
from enum import Enum

from connectfour.pubsub import ModelAction, ViewAction

DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7
DEFAULT_TO_WIN = 4


class ConnectFourModel(object):
    """Top-level model for the Connect Four game.

    This model supports numbers other than Four (Connect Three, Six, etc.), as
    well as variable board dimensions and a variable number of players.

    Dependencies between the core methods:

    -   _create_board(), _add_player(), and _remove_player() cannot be called
        when a game is in progress. There must be a board created and a player
        added before calling _start_game().

    -   _add_player() can be called multiple times to add multiple players.
        Since each player must have a distinct color, the number of players is
        capped at len(Color).

    -   If _create_board() is called more than once, the old board is replaced
        with the new board.

    -   If _start_game() is called while a game is in progress, it resets the
        previous game.

    -   _play() can only be called while a game is in progress.
    """

    def __init__(self, pubsub):
        """Create this model."""
        self.pubsub = pubsub
        self.board = None
        self.players = []
        self.used_colors = set()

        self.game_in_progress = False
        self.game_number = 0

        # After being incremented, which player goes first in the next game
        self.first_player_index = -1

        # Which player goes next in the current game
        self.current_player_index = 0

        self._create_subscriptions()

    def _create_subscriptions(self):
        responses = {
            ViewAction.create_board: self._create_board,
            ViewAction.add_player: self._add_player,
            ViewAction.remove_player: self._remove_player,
            ViewAction.start_game: self._start_game,
            ViewAction.play: self._play,
            ViewAction.request_ai_play: self._do_ai_play,
        }

        for action, response in responses.iteritems():
            self.pubsub.subscribe(action, response)

    def __repr__(self):
        return 'ConnectFourModel board={}, num_players={}'.format(
            self.board, self.get_num_players())

    def get_json_board(self):
        if self.board:
            return self.board.get_json()
        else:
            return None

    def get_json_players(self):
        return [p.get_json() for p in self.players]

    def _create_board(self, num_rows=DEFAULT_ROWS, num_columns=DEFAULT_COLUMNS,
                      num_to_win=DEFAULT_TO_WIN):
        """Add a playing board.

        Publishes a board_created ModelAction.

        If a board was previously created, it is replaced with this board.

        Args:
            num_rows (Optional[int]): Number of rows in the board.
                Must be positive.
            num_columns (Optional[int]): Number of columns in the board.
                Must be positive.
            num_to_win (Optional[int]): Number in a row to win.
                Must be positive.
        Raises:
            RuntimeError: If a game is currently in progress.
            ValueError: If either dimension or the num_to_win is less than 1.
        """
        if self.game_in_progress:
            raise RuntimeError('Cannot add board while a game is in progress')

        if num_rows < 1 or num_columns < 1 or num_to_win < 1:
            raise ValueError('Board dimensions and num_to_win must be >= 1')

        self.board = Board(num_rows, num_columns, num_to_win)
        self.pubsub.publish(ModelAction.board_created, board=self.board)

    def _add_player(self, name, color=None, is_ai=False, pk=None):
        """Add a player.

        Publishes a player_added ModelAction.

        Args:
            name (str): The player's name. Must be non-empty. Does not need
                to be unique (two Emilys are distinguishable by color).
            color (Optional[Color]): This player's playing color. Must be
                unique. Defaults to next available color.
            is_ai (Optional[bool]): Whether this player is AI.
            pk (Optional): An identifier for this player. While not required,
                might be useful in a view.

        Raises:
            RuntimeError: If a game is currently in progress.
            ValueError: If name is empty or if color is already in use.
        """
        if self.game_in_progress:
            raise RuntimeError('Cannot add player while a game is in progress')

        if not name:
            raise ValueError('Name is required and must be non-empty')

        if color in self.used_colors:
            raise ValueError('Color {} is already used'.format(color))

        if not color:
            color = self._get_unassigned_color()
            if not color:
                raise ValueError('All colors taken')

        self.used_colors.add(color)
        player = Player(name=name, color=color, is_ai=is_ai, pk=pk)
        self.players.append(player)
        self.pubsub.publish(ModelAction.player_added, player=player)

    def _get_unassigned_color(self):
        if len(self.used_colors) == len(Color):
            return None

        for color in get_all_colors():
            if color not in self.used_colors:
                return color

        return None

    def _remove_player(self, player):
        """Remove a player.

        Publishes a player_removed ModelAction.

        Args:
            player (Player): The player to be removed.
        Raises:
            RuntimeError: If a game is currently in progress.
            ValueError: If player not currently in the model.
        """
        if self.game_in_progress:
            raise RuntimeError('Cannot remove player while a game is in '
                               'progress')

        if player not in self.players:
            raise ValueError('Player {} not in this model'.format(player))

        self.players.remove(player)
        self.used_colors.remove(player.color)
        self.pubsub.publish(ModelAction.player_removed, player=player)

    def _start_game(self):
        """Start a new game.

        Publishes a game_started ModelAction, followed by a next_player Action
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

        self._increment_first_player_index()
        self.current_player_index = self.first_player_index

        self.board.reset()
        self.game_in_progress = True
        self.game_number += 1
        self.pubsub.publish(
            ModelAction.game_started, game_number=self.game_number)

        self._process_next_player()

    def _play(self, column):
        """Play in a column.

        The play is assumed to be by the current player.

        If the play is illegal, publishes a try_again ModelAction. Otherwise,
        publishes a color_played ModelAction, followed by one of the following
        (depending on the outcome): game_won, game_draw, or next_player.

        Args:
            column (int): The column to play in.
        Raises:
            RuntimeError: If a game is not currently in progress.
        """
        if not self.game_in_progress:
            raise RuntimeError('Cannot play before game has started')

        if not self.board.is_column_in_bounds(column):
            self.pubsub.publish(
                ModelAction.try_again, player=self.get_current_player(),
                reason=TryAgainReason.column_out_of_bounds)

        elif self.board.is_column_full(column):
            self.pubsub.publish(
                ModelAction.try_again, player=self.get_current_player(),
                reason=TryAgainReason.column_full)

        else:
            self.process_play(column)

    def _do_ai_play(self):
        player = self.get_current_player()
        player.do_strategy(self)

    def process_play(self, column):
        player = self.get_current_player()
        row = self.board.add_color(player.color, column)
        self.pubsub.publish(
            ModelAction.color_played, color=player.color,
            position=(row, column))

        winning_positions = self.board.get_winning_positions((row, column))

        if winning_positions:
            self._process_win(player, winning_positions)
        elif self.board.is_full():
            self._process_draw()
        else:
            self._increment_current_player_index()
            self._process_next_player()

    def _process_win(self, winner, winning_positions):
        self.game_in_progress = False
        self._increment_num_games_all_players()
        winner.num_wins += 1
        self.pubsub.publish(
            ModelAction.game_won, winner=winner,
            winning_positions=winning_positions)

    def _process_draw(self):
        self.game_in_progress = False
        self._increment_num_games_all_players()
        self.pubsub.publish(ModelAction.game_draw)

    def _process_next_player(self):
        player = self.get_current_player()
        self.pubsub.publish(ModelAction.next_player, player=player)

    def _increment_current_player_index(self):
        self.current_player_index = ((self.current_player_index + 1)
                                     % self.get_num_players())

    def _increment_first_player_index(self):
        self.first_player_index = ((self.first_player_index + 1)
                                   % self.get_num_players())

    def _increment_num_games_all_players(self):
        for player in self.players:
            player.num_games += 1

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
        if self.board:
            return self.board.get_printable_grid(**kwargs)
        else:
            return ''


class Color(Enum):
    """A color for a player to play in the board."""

    # Yellow omitted to serve as background color (as in the classic game).
    (black, red, blue, purple, green, brown, pink, gray, orange,
        lime) = range(10)


def get_all_colors():
    for color in Color:
        yield color


class TryAgainReason(Enum):
    """Reason that a player needs to try again."""

    column_out_of_bounds, column_full = range(2)


AI_EASY = 'easy'
AI_MEDIUM = 'medium'
AI_HARD = 'hard'


class Player(object):
    """A Connect Four player."""

    def __init__(self, name, color, is_ai=False, pk=None):
        """Create a player.

        Args:
            name (str): This player's name.
            color (Color): This player's playing color.
            is_ai (Optional[bool]): Whether this player is AI.
            pk (Optional): An identifier for this player. While not required,
                might be useful in a view.
        """
        self.name = name
        self.color = color
        self.is_ai = is_ai
        self.pk = pk
        self.num_wins = 0
        self.num_games = 0

        if self.is_ai:
            self.difficulty = AI_HARD

    def __repr__(self):
        return '{} name={} color={} is_ai={} pk={}'.format(
            self.__class__.__name__, self.name, self.color, self.pk,
            self.is_ai)

    def __str__(self):
        category = 'AI' if self.is_ai else 'Human'
        return '{} ({}): {}'.format(self.name, self.color.name, category)

    def get_json(self):
        return {
            'name': self.name,
            'color': self.color.name,
            'isAI': self.is_ai,
            'pk': self.pk,
            'numWins': self.num_wins,
            'numGames': self.num_games,
        }

    def do_strategy(self, model):
        AI_STRATEGIES = {
            AI_EASY: self.easy_ai_strategy,
            AI_MEDIUM: self.medium_ai_strategy,
            AI_HARD: self.hard_ai_strategy,
        }

        column = AI_STRATEGIES[self.difficulty](model)
        model.process_play(column)

    def easy_ai_strategy(self, model):
        return self.find_random_legal_column(model)

    def medium_ai_strategy(self, model):
        column = self.find_win(model)
        if column is not None:
            return column

        return self.find_random_legal_column(model)

    def hard_ai_strategy(self, model):
        column = self.find_win(model)
        if column is not None:
            return column

        column = self.prevent_win(model)
        if column is not None:
            return column

        return self.find_random_legal_column(model)

    def find_random_legal_column(self, model):
        columns = [c for c in range(model.get_num_columns())
                   if not model.board.is_column_full(c)]
        return random.choice(columns)

    def find_win(self, model):
        columns = [c for c in range(model.get_num_columns())
                   if not model.board.is_column_full(c)]
        color = self.color

        for column in columns:
            row = model.board.find_next_row(column)
            if model.board.get_winning_positions(
                    (row, column), fake_color=color):
                return column

        return None

    def prevent_win(self, model):
        columns = [c for c in range(model.get_num_columns())
                   if not model.board.is_column_full(c)]

        for column in columns:
            row = model.board.find_next_row(column)

            # TODO: order this in playing order
            for player in model.players:
                if model.board.get_winning_positions(
                        (row, column), fake_color=player.color):
                    return column

        return None


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

    def get_json(self):
        new_grid = []

        for row in self.grid:
            new_row = []
            for item in row:
                if item:
                    new_row.append(item.name)
                else:
                    new_row.append(None)
            new_grid.append(new_row)

        return {
            'numRows': self.num_rows,
            'numColumns': self.num_columns,
            'numToWin': self.num_to_win,
            'grid': new_grid,
        }

    def reset(self):
        """Reset this board for a new game.

        Sets all positions in this board's grid to None.
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                self.grid[row][column] = None

    def find_next_row(self, column):
        """Find the row where a disc would land if played in this column."""
        if not self.is_column_in_bounds(column):
            raise ValueError('Column {} out of bounds'.format(column))

        if self.is_column_full(column):
            raise ValueError('Column {} is full'.format(column))

        current_row = self.bottom_row

        while self.get_color((current_row, column)) is not None:
            current_row -= 1

        return current_row

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
        row = self.find_next_row(column)
        self.grid[row][column] = color
        return row

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

    def _get_matches_mirrored(self, start, step, fake_color=None):
        """
        From start position, find positions with matching color outward in the
        direction indicated by step as well as in the 180-flipped direction.
        Returns a set of the matching positions, including start.
        """
        flipped_step = tuple(-i for i in step)

        a = self._get_matches(start, step, fake_color=fake_color)
        b = self._get_matches(start, flipped_step, fake_color=fake_color)

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
