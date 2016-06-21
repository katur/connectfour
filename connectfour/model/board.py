import operator

TOP_ROW = 0
LEFT_COLUMN = 0

HORIZONTAL = (0, 1)
VERTICAL = (1, 0)
UP_RIGHT = (1, 1)
DOWN_RIGHT = (1, -1)


class ConnectFourBoard(object):
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

        self.top_row = TOP_ROW
        self.bottom_row = num_rows - 1
        self.left_column = LEFT_COLUMN
        self.right_column = num_columns - 1

        self.grid = [[None for column in range(num_columns)]
                     for row in range(num_rows)]

    def __str__(self):
        return '{} rows x {} columns ({} to win)'.format(
            self.num_rows, self.num_columns, self.num_to_win)

    def __repr__(self):
        return self.__str__()

    def get_printable_grid(self, field_width=None):
        """Get a "pretty" string of this board's grid.

        Might be used for console printing.

        Args:
            field_width (Optional[int]): The number of spaces each disc
                should take up.

        Returns:
            str: A tab- and new-line formatted string of the grid.
        """
        output = ''
        for row in self.grid:
            for column in row:
                el = column if column else '-'
                if field_width:
                    output += '{0:{width}}'.format(el, width=field_width)
                else:
                    output += '{0}\t'.format(el)
            output += '\n'

        return output

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

    def reset(self):
        """Reset this board for a new game.

        Sets all positions in this board's grid to None.
        """
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                self.grid[row][column] = None

    def get_disc(self, position):
        """Retrieve a disc from this board.

        Args:
            position: A 2-tuple in format (row, column).
        Returns:
            ConnectFourDisc: The disc at this position, or None if this
                position is empty.
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
            disc (ConnectFourDisc): The disc to add.
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
            fake_disc (Optional[ConnectFourDisc]): A disc to pretend is
                at start. Might be used to predict whether a win might
                occur without actually playing the disc.
        Returns:
            set: A set of 2-tuples in format (row, column) of the positions
                that result in a win, or the empty set if no win found.
        """
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

            fake_disc (Optional[ConnectFourDisc]): See docstring for
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

            fake_disc (Optional[ConnectFourDisc]): See docstring for
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
