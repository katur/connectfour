import unittest

from connectfour.model import Board, Color

TEST_ROWS = 4
TEST_COLUMNS = 6
TEST_TO_WIN = 4

PINK = Color.pink
BLUE = Color.blue
GRAY = Color.gray

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)

PLAYS = {
    'BOARD-A': [
        (BLUE, 0), (GRAY, 0), (GRAY, 0),
        (PINK, 1),
        (BLUE, 2), (PINK, 2), (BLUE, 2), (PINK, 2),
        (BLUE, 3), (PINK, 3), (PINK, 3), (BLUE, 3),
        (BLUE, 4), (PINK, 4), (PINK, 4), (BLUE, 4),
        (PINK, 5),
    ],
}
"""Test plays for a board with TEST_ROWS, TEST_COLUMNS, TEST_TO_WIN.

BOARD-A looks like:

                    pink    blue    blue
    gray            blue    pink    pink
    gray            pink    pink    pink
    blue    pink    blue    blue    blue    pink
"""


class TestBoard_Basics(unittest.TestCase):

    def setUp(self):
        self.board = Board(TEST_ROWS, TEST_COLUMNS, TEST_TO_WIN)

        self.bottom_row = self.board.bottom_row
        self.top_row = self.board.top_row
        self.left_column = self.board.left_column
        self.right_column = self.board.right_column

        self.bottom_left = (self.bottom_row, self.left_column)
        self.bottom_right = (self.bottom_row, self.right_column)
        self.top_left = (self.top_row, self.left_column)
        self.top_right = (self.top_row, self.right_column)

    def test_board_to_win(self):
        self.assertEqual(self.board.num_to_win, TEST_TO_WIN)

    def test_board_dimensions(self):
        self.assertEqual(self.board.num_rows, TEST_ROWS)
        self.assertEqual(self.board.num_columns, TEST_COLUMNS)

    def test_grid_dimensions(self):
        self.assertEqual(len(self.board.grid), TEST_ROWS)
        self.assertEqual(len(self.board.grid[0]), TEST_COLUMNS)

    def test_board_extremes(self):
        self.assertEqual(self.left_column, 0)
        self.assertEqual(self.right_column, TEST_COLUMNS - 1)
        self.assertEqual(self.top_row, 0)
        self.assertEqual(self.bottom_row, TEST_ROWS - 1)

    def test_grid_size(self):
        num_positions = 0
        for i in self.board.grid:
            for j in i:
                num_positions += 1
        self.assertEqual(num_positions, TEST_ROWS * TEST_COLUMNS)

    def test_is_row_in_bounds(self):
        self.assertTrue(self.board.is_row_in_bounds(self.top_row))
        self.assertTrue(self.board.is_row_in_bounds(self.bottom_row))
        self.assertFalse(self.board.is_row_in_bounds(self.top_row - 1))
        self.assertFalse(self.board.is_row_in_bounds(self.bottom_row + 1))

    def test_is_column_in_bounds(self):
        self.assertTrue(self.board.is_column_in_bounds(self.left_column))
        self.assertTrue(self.board.is_column_in_bounds(self.right_column))
        self.assertFalse(self.board.is_column_in_bounds(self.left_column - 1))
        self.assertFalse(self.board.is_column_in_bounds(self.right_column + 1))

    def test_is_in_bounds(self):
        self.assertTrue(self.board.is_in_bounds(self.bottom_left))
        self.assertTrue(self.board.is_in_bounds(self.bottom_right))
        self.assertTrue(self.board.is_in_bounds(self.top_left))
        self.assertTrue(self.board.is_in_bounds(self.top_right))

        self.assertFalse(self.board.is_in_bounds(
            (self.top_row, self.right_column + 1)))
        self.assertFalse(self.board.is_in_bounds(
            (self.bottom_row + 1, self.right_column)))
        self.assertFalse(self.board.is_in_bounds(
            (self.bottom_row, self.left_column - 1)))
        self.assertFalse(self.board.is_in_bounds(
            (self.top_row - 1, self.left_column)))

    def test_add_and_get_one_color_left_column(self):
        self.board.add_color(BLUE, self.left_column)
        self.assertEqual(BLUE, self.board.get_color(self.bottom_left))
        self.assertIsNone(self.board.get_color(self.bottom_right))

    def test_add_and_get_one_color_right_column(self):
        self.board.add_color(BLUE, self.right_column)
        self.assertEqual(BLUE, self.board.get_color(self.bottom_right))
        self.assertIsNone(self.board.get_color(self.bottom_left))

    def test_add_color_out_of_bounds_left(self):
        with self.assertRaises(ValueError):
            self.board.add_color(BLUE, self.left_column - 1)

    def test_add_color_out_of_bounds_right(self):
        with self.assertRaises(ValueError):
            self.board.add_color(BLUE, self.right_column + 1)

    def test_is_column_full_when_empty(self):
        self.assertFalse(self.board.is_column_full(self.left_column))

    def test_is_column_full_when_only_one(self):
        self.board.add_color(BLUE, self.left_column)
        self.assertFalse(self.board.is_column_full(self.left_column))

    def test_is_column_full_when_missing_one(self):
        for i in range(self.board.num_rows - 1):
            self.board.add_color(BLUE, self.left_column)
        self.assertFalse(self.board.is_column_full(self.left_column))

    def test_is_column_full_when_full(self):
        for i in range(self.board.num_rows):
            self.board.add_color(BLUE, self.left_column)
        self.assertTrue(self.board.is_column_full(self.left_column))

    def test_is_column_full_out_of_bounds_left(self):
        with self.assertRaises(ValueError):
            self.board.is_column_full(self.left_column - 1)

    def test_is_column_full_out_of_bounds_right(self):
        with self.assertRaises(ValueError):
            self.board.is_column_full(self.right_column + 1)

    def test_is_board_full_when_empty(self):
        self.assertFalse(self.board.is_full())

    def test_is_board_full_when_only_one(self):
        self.board.add_color(BLUE, self.left_column)
        self.assertFalse(self.board.is_full())

    def test_is_board_full_when_missing_one(self):
        # Fill entire board except last column
        for column in range(self.board.num_columns - 1):
            for row in range(self.board.num_rows):
                self.board.add_color(BLUE, column)

        # Fill last column except for top row
        for row in range(self.board.num_rows - 1):
            self.board.add_color(BLUE, self.right_column)

        self.assertFalse(self.board.is_full())

    def test_is_board_full_when_full(self):
        _fill_board_pink(self.board)
        self.assertTrue(self.board.is_full())

    def test_reset_empty_board(self):
        self.assertTrue(_is_empty(self.board))
        self.board.reset()
        self.assertTrue(_is_empty(self.board))

    def test_reset_partial_board(self):
        # Fill left and right columns (to get all corners)
        for row in range(self.board.num_rows):
            self.board.add_color(BLUE, self.left_column)
            self.board.add_color(BLUE, self.right_column)

        self.assertFalse(_is_empty(self.board))
        self.board.reset()
        self.assertTrue(_is_empty(self.board))

    def test_reset_full_board(self):
        _fill_board_pink(self.board)
        self.assertFalse(_is_empty(self.board))
        self.board.reset()
        self.assertTrue(_is_empty(self.board))


class TestBoard_MatchesAndWins_A(unittest.TestCase):

    def setUp(self):
        self.board = Board(TEST_ROWS, TEST_COLUMNS, TEST_TO_WIN)

        for play in PLAYS['BOARD-A']:
            self.board.add_color(*play)

    def test_matches(self):
        m = self.board._get_matches((3, 3), RIGHT)
        self.assertEquals(m, {(3, 3), (3, 4)})

    def test_matches_one_only(self):
        m = self.board._get_matches((2, 2), LEFT)
        self.assertEquals(m, {(2, 2)})

    def test_matches_mirrored_both_dir_relevant(self):
        m = self.board._get_matches_mirrored((2, 3), RIGHT)
        n = self.board._get_matches_mirrored((2, 3), LEFT)
        self.assertEquals(m, n)
        self.assertEquals(m, {(2, 2), (2, 3), (2, 4)})

    def test_matches_mirrored_one_dir_relevant(self):
        m = self.board._get_matches_mirrored((2, 2), RIGHT)
        n = self.board._get_matches_mirrored((2, 2), LEFT)
        self.assertEquals(m, n)
        self.assertEquals(m, {(2, 2), (2, 3), (2, 4)})

    def test_winning_positions_diagonal_both_dir_relevant(self):
        w = self.board.get_winning_positions((2, 4))
        self.assertEquals(w, {(0, 2), (1, 3), (2, 4), (3, 5)})

    def test_winning_positions_diagonal_only_one_dir_relevant(self):
        w = self.board.get_winning_positions((3, 5))
        self.assertEquals(w, {(0, 2), (1, 3), (2, 4), (3, 5)})

    def test_winning_positions_with_fake(self):
        w = self.board.get_winning_positions((2, 1), fake_color=PINK)
        self.assertEquals(w, {(2, 1), (2, 2), (2, 3), (2, 4)})


###########
# Helpers #
###########

def _is_empty(board):
    for row in range(board.num_rows):
        for column in range(board.num_columns):
            if board.grid[row][column]:
                return False
    return True


def _fill_board_pink(board):
    for column in range(board.num_columns):
        for row in range(board.num_rows):
            board.add_color(BLUE, column)
