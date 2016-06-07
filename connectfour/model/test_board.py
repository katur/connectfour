import unittest
from board import Board
from disc import Disc


TEST_NUM_ROWS = 4
TEST_NUM_COLUMNS = 6
PINK = Disc('pink')
BROWN = Disc('brown')


class EmptyBoardTestCase(unittest.TestCase):

    def setUp(self):
        self.board = Board(TEST_NUM_ROWS, TEST_NUM_COLUMNS)
        self.bottom_left = (self.board.bottom_row, self.board.left_column)
        self.bottom_right = (self.board.bottom_row, self.board.right_column)

    def test_board_dimensions(self):
        self.assertEqual(self.board.num_rows, TEST_NUM_ROWS)
        self.assertEqual(self.board.num_columns, TEST_NUM_COLUMNS)

    def test_grid_dimensions(self):
        self.assertEqual(len(self.board.grid), TEST_NUM_ROWS)
        self.assertEqual(len(self.board.grid[0]), TEST_NUM_COLUMNS)

    def test_add_disc_out_of_bounds_left(self):
        with self.assertRaises(ValueError):
            self.board.add_disc(PINK, -1)

    def test_add_disc_out_of_bounds_right(self):
        with self.assertRaises(ValueError):
            self.board.add_disc(PINK, self.board.num_columns)

    def test_add_and_get_one_disc_left_column(self):
        self.board.add_disc(PINK, 0)
        self.assertEqual(PINK, self.board.get_disc(self.bottom_left))
        self.assertIsNone(self.board.get_disc(self.bottom_right))

    def test_add_and_get_one_disc_right_column(self):
        self.board.add_disc(PINK, self.board.num_columns - 1)
        self.assertEqual(PINK, self.board.get_disc(self.bottom_right))
        self.assertIsNone(self.board.get_disc(self.bottom_left))
