TOP_ROW = 0
LEFT_COLUMN = 0


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
        current_disc = self.get_disc(current_row, column)

        while current_disc is not None:
            current_row -= 1
            current_disc = self.get_disc(current_row, column)

        self.grid[current_row][column] = disc
