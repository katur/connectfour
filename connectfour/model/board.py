import operator

TOP_ROW = 0
LEFT_COLUMN = 0

HORIZONTAL = (0, 1)
VERTICAL = (1, 0)
UP_RIGHT = (1, 1)
DOWN_RIGHT = (1, -1)


class Board(object):
    """A Connect Four playing board."""

    def __init__(self, num_rows, num_columns, num_to_win):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_to_win = num_to_win
        self.top_row = TOP_ROW
        self.bottom_row = num_rows - 1
        self.left_column = LEFT_COLUMN
        self.right_column = num_columns - 1

        self.grid = [[None for column in range(num_columns)]
                     for row in range(num_rows)]

    def __str__(self):
        return '{} rows x {} column Board ({} to win)'.format(
            self.num_rows, self.num_columns, self.num_to_win)

    def __repr__(self):
        return self.__str__()

    def get_printable_grid(self):
        """Get a string of this board's grid.

        Might be used for console printing.
        """
        s = ''
        for row in self.grid:
            for column in row:
                if column:
                    s += '{}\t'.format(column)
                else:
                    s += '-\t'
            s += '\n'

        return s

    def is_row_in_bounds(self, row):
        """Determine if row is in bounds."""
        return row >= self.top_row and row <= self.bottom_row

    def is_column_in_bounds(self, column):
        """Determine if column is in bounds."""
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
            column: An int of the column to check.
        Returns:
            bool: True if column is full, False otherwise.
        Raises:
            ValueError: If column is out of bounds.
        """
        if not self.is_column_in_bounds(column):
            raise ValueError('Column {} is out of bounds'.format(column))

        return self.grid[self.top_row][column] is not None

    def is_full(self):
        """Determine if this board is entirely full of discs."""
        for i in range(self.num_columns):
            if not self.is_column_full(i):
                return False

        return True

    def reset(self):
        """Reset this board for a new game.

        Sets all positions in the board's grid to None.
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                self.grid[row][column] = None

    def get_disc(self, position):
        """Retrieve a disc from this board.

        Args:
            position: A 2-tuple in format (row, column).
        Returns:
            Disc: The disc at this position in the board.
        Raises:
            ValueError: If position is out of bounds.
        """
        if not self.is_in_bounds(position):
            raise ValueError('Position {} is out of bounds'
                             .format(position))

        row, column = position
        return self.grid[row][column]

    def add_disc(self, disc, column):
        """Add a disc to a column.

        Args:
            disc: The Disc to add.
            column: An int of the column to add the disc to.
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

    def _get_consecutive_matches(self, start, step, fake_disc=None):
        """Get consecutive matching positions in a single direction.

        From a starting position, find positions with discs matching that
        in the starting position, outward in the direction indicated by step,
        until a mismatch is found.

        Args:
            start: A 2-tuple (row, column) of starting position.
            step: A 2-tuple (vertical_step, horizontal_step) indicating
                the direction to move with each step.

                For example, to check upwards, step should be (1, 0).
                To check diagonally down-left, step should be (-1, -1).

            fake_disc (Optional): A disc to pretend to place at start.
                Might be used to predict whether a win might occur before
                actually playing the disc.
        Returns:
            set: A set of 2-tuples in format (row, column) of the matching
                positions. This set includes the starting position. Thus,
                if no matches are found, the set contains only the starting
                position.
        """
        disc = fake_disc if fake_disc else self.get_disc(start)

        # Initialize set with start position
        positions = {start}

        current = tuple(map(operator.add, start, step))

        while (self.is_in_bounds(current) and self.get_disc(current) == disc):
            positions.add(current)
            current = tuple(map(operator.add, current, step))

        return positions

    def _get_consecutive_matches_mirrored(self, start, step, fake_disc=None):
        """Get consecutive matching positions in two directions.

        From a starting position, find positions with discs matching the
        starting position, outward in the direction indicated by step,
        as well as outward in the 180-flipped direction, until a mismatch
        is found.

        Args:
            start: A 2-tuple (row, column) of starting position.
            step: A 2-tuple (vertical_step, horizontal_step), indicating
                the direction to move with each step. The 180-degree
                rotation of this step will be included as well.

                For example, to check the horizontal axis, step can be
                either (0, 1) or (0, -1).

            fake_disc (Optional): A disc to pretend to place at start.
                Might be used to predict whether a win might occur before
                actually playing the disc.
        Returns:
            set: A set of 2-tuples in format (row, column) of the matching
                positions. This set includes the starting position. Thus,
                if no matches are found, the set contains only the starting
                position.
        """
        flipped_step = tuple(-i for i in step)

        a = self._get_consecutive_matches(start, step, fake_disc=fake_disc)
        b = self._get_consecutive_matches(start, flipped_step,
                                          fake_disc=fake_disc)

        return a | b

    def get_winning_positions(self, origin, fake_disc=None):
        """Get winning positions that include the origin position.

        Args:
            origin: A 2-tuple (row, column)
            fake_disc (Optional): A disc to pretend to place at start. Might
                be used to predict whether a win might occur.
        Returns:
            set: A set of 2-tuples in format (row, column) of the winning
                positions. Returns the empty set if no win found.
        """
        winning_positions = set()

        for step in (HORIZONTAL, VERTICAL, UP_RIGHT, DOWN_RIGHT):
            matches = self._get_consecutive_matches_mirrored(
                origin, step, fake_disc=fake_disc)

            # Check if these matches are enough to win
            if len(matches) >= self.num_to_win:
                winning_positions |= matches

        return winning_positions
