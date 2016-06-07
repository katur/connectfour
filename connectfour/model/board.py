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
        self.grid = [[None for y in range(num_columns)]
                     for x in range(num_rows)]

        self.top_row = TOP_ROW
        self.bottom_row = num_rows - 1
        self.left_column = LEFT_COLUMN
        self.right_column = num_columns - 1

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
                    s += '{}\t'.format(column.color)
                else:
                    s += '-\t'
            s += '\n'

        return s

    def get_disc(self, row, column):
        """
        Get the disc at this row and column.
        """
        return self.grid[row][column]

    def is_in_bounds(self, row, column):
        return (row >= self.top_row and row <= self.bottom_row and
                column >= self.left_column and column <= self.right_column)

    def is_column_full(self, column):
        """
        Determine if a column is full of discs.
        """
        return self.grid[TOP_ROW][column] is not None

    def add_disc(self, disc, column):
        """
        Add a disc to a column.
        """
        if (column < LEFT_COLUMN) or (column >= self.num_columns):
            raise ValueError('Column {} out of bounds'.format(column))

        if self.is_column_full(column):
            raise ValueError('Column {} is full'.format(column))

        current_row = self.bottom_row

        while self.get_disc(current_row, column) is not None:
            current_row -= 1

        self.grid[current_row][column] = disc

    def get_num_outward_discs_1D(self, disc, row, column, step):
        """
        Get the number of consecutive disc matches, stepping outward
        from position [row, column] (exclusive), in a single direction.

        step should be a 2-tuple, (horizontal_step, vertical_step).

        For example, to check upwards, step should be (0, 1).
        To check diagonally down-left, step should be (-1, -1).
        """
        current = (row + step[0], column + step[1])
        total = 0

        while (self.is_in_bounds(*current) and
                self.get_disc(*current) == disc):
            total += 1
            current = (current[0] + step[0], current[1] + step[1])

        return total

    def get_num_outward_discs_2D(self, disc, row, column, step):
        """
        Get the number of consecutive disc matches, stepping outward
        from position [row, column] (exclusive), in two directions.

        step should be a 2-tuple, (horizontal_step, vertical_step),
        and the mirror of this step is checked as well.

        For example, to check the horizontal axis, step could be
        (0, 1) or (0, -1).
        To check the up-right/down-left diagonal, step could be
        (1, 1) or (-1, -1).
        """
        mirror = (-step[0], -step[1])

        a = self.get_num_outward_discs_1D(disc, row, column, step)
        b = self.get_num_outward_discs_1D(disc, row, column, mirror)

        return a + b

    def check_for_win(self, disc, row, column, win):
        """
        Check for a win if disc were placed at position [row, column].
        """
        for step in (HORIZONTAL, VERTICAL, UP_RIGHT, DOWN_RIGHT):
            x = self.get_num_outward_discs_2D(disc, row, column, step)
            if x + 1 >= win:
                return True

        return False
