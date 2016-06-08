TOP_ROW = 0
LEFT_COLUMN = 0

HORIZONTAL = (0, 1)
VERTICAL = (1, 0)
UP_RIGHT = (1, 1)
DOWN_RIGHT = (1, -1)


class Board(object):
    """
    A Connect Four playing board.
    """

    def __init__(self, num_rows, num_columns):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.top_row = TOP_ROW
        self.bottom_row = num_rows - 1
        self.left_column = LEFT_COLUMN
        self.right_column = num_columns - 1

        self.grid = [[None for y in range(num_columns)]
                     for x in range(num_rows)]

    def __str__(self):
        return '{} x {} Board'.format(self.num_rows, self.num_columns)

    def __repr__(self):
        return self.__str__()

    def get_printable_grid(self):
        """
        Get a string of the grid meant for console printing.
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

    def get_disc(self, position):
        """
        Get the disc at this position.

        Position should be a 2-tuple in format (x, y).
        """
        x, y = position
        return self.grid[x][y]

    def is_in_bounds(self, position):
        """
        Determine whether position is in bounds.

        Position should be a 2-tuple in format (x, y).
        """
        x, y = position
        return (x >= self.top_row and x <= self.bottom_row and
                y >= self.left_column and y <= self.right_column)

    def is_column_full(self, column):
        """
        Determine if a column is full of discs.
        """
        return self.grid[self.top_row][column] is not None

    def add_disc(self, disc, column):
        """
        Add a disc to a column.
        """
        if column < self.left_column or column > self.right_column:
            raise ValueError('Column {} out of bounds'.format(column))

        if self.is_column_full(column):
            raise ValueError('Column {} is full'.format(column))

        current_row = self.bottom_row

        while self.get_disc((current_row, column)) is not None:
            current_row -= 1

        self.grid[current_row][column] = disc

    def get_consecutive_matches(self, disc, start, step):
        """
        Get a set of the consecutive positions matching disc,
        stepping outward from start (exclusive)
        in a single direction (indicated by step).

        start should be a 2-tuple (x, y) of the starting position.

        step should be a 2-tuple, (horizontal_step, vertical_step).
        For example, to check upwards, step should be (0, 1).
        To check diagonally down-left, step should be (-1, -1).
        """
        current = (start[0] + step[0], start[1] + step[1])
        positions = set()

        while (self.is_in_bounds(current) and self.get_disc(current) == disc):
            positions.add(current)
            current = (current[0] + step[0], current[1] + step[1])

        return positions

    def get_consecutive_matches_mirrored(self, disc, start, step):
        """
        Get a set of the consecutive positions matching disc,
        stepping outward from start (exclusive)
        in two directions (step and its mirror).

        start should be a 2-tuple (x, y) of the starting position.

        step should be a 2-tuple, (horizontal_step, vertical_step),
        and the mirror of this step will be used as well.
        For example, to check the horizontal axis, step could be
        (0, 1) or (0, -1).
        To check the up-right/down-left diagonal, step could be
        (1, 1) or (-1, -1).
        """
        mirrored_step = (-step[0], -step[1])

        a = self.get_consecutive_matches(disc, start, step)
        b = self.get_consecutive_matches(disc, start, mirrored_step)

        return a | b

    def get_winning_positions(self, origin, number_to_win,
                              fake_disc=None):
        """
        Get a set of winning positions including the disc
        at origin.

        Optionally supply argument fake_disc to pretend that that
        disc were placed at origin.

        If a win including origin is not present, returns an empty set.
        """
        winning_positions = set()

        if fake_disc:
            disc = fake_disc
        else:
            disc = self.get_disc(origin)

        for step in (HORIZONTAL, VERTICAL, UP_RIGHT, DOWN_RIGHT):
            matches = self.get_consecutive_matches_mirrored(
                disc, origin, step)

            # Check if these matches, with the origin, wins
            if len(matches) + 1 >= number_to_win:
                winning_positions |= matches

        # If any win was found, add origin to the set
        if winning_positions:
            winning_positions.add(origin)

        return winning_positions
