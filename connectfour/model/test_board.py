import unittest

from board import Board
from color import Color
from disc import Disc

TEST_NUM_ROWS = 4
TEST_NUM_COLUMNS = 6
TEST_NUM_TO_WIN = 4
PINK = Disc(Color.pink)
BROWN = Disc(Color.brown)


class TestBoardBasics(unittest.TestCase):

    def setUp(self):
        self.board = Board(TEST_NUM_ROWS, TEST_NUM_COLUMNS, TEST_NUM_TO_WIN)

        self.bottom_row = self.board.bottom_row
        self.top_row = self.board.top_row
        self.left_column = self.board.left_column
        self.right_column = self.board.right_column

        self.bottom_left = (self.bottom_row, self.left_column)
        self.bottom_right = (self.bottom_row, self.right_column)
        self.top_left = (self.top_row, self.left_column)
        self.top_right = (self.top_row, self.right_column)

    def test_board_dimensions(self):
        self.assertEqual(self.board.num_rows, TEST_NUM_ROWS)
        self.assertEqual(self.board.num_columns, TEST_NUM_COLUMNS)

    def test_grid_dimensions(self):
        self.assertEqual(len(self.board.grid), TEST_NUM_ROWS)
        self.assertEqual(len(self.board.grid[0]), TEST_NUM_COLUMNS)

    def test_board_extremes(self):
        self.assertEqual(self.left_column, 0)
        self.assertEqual(self.right_column, TEST_NUM_COLUMNS - 1)
        self.assertEqual(self.top_row, 0)
        self.assertEqual(self.bottom_row, TEST_NUM_ROWS - 1)

    def test_grid_size(self):
        num_positions = 0
        for i in self.board.grid:
            for j in i:
                num_positions += 1
        self.assertEqual(num_positions, TEST_NUM_ROWS * TEST_NUM_COLUMNS)

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

    def test_is_column_full_out_of_bounds_left(self):
        with self.assertRaises(ValueError):
            self.board.is_column_full(self.left_column - 1)

    def test_is_column_full_out_of_bounds_right(self):
        with self.assertRaises(ValueError):
            self.board.is_column_full(self.right_column + 1)

    def test_is_column_full_when_empty(self):
        self.assertFalse(self.board.is_column_full(self.left_column))

    def test_is_column_full_when_only_one(self):
        self.board.add_disc(PINK, self.left_column)
        self.assertFalse(self.board.is_column_full(self.left_column))

    def test_is_column_full_when_full(self):
        for i in range(self.board.num_rows):
            self.board.add_disc(PINK, self.left_column)
        self.assertTrue(self.board.is_column_full(self.left_column))

    def test_add_disc_out_of_bounds_left(self):
        with self.assertRaises(ValueError):
            self.board.add_disc(PINK, self.left_column - 1)

    def test_add_disc_out_of_bounds_right(self):
        with self.assertRaises(ValueError):
            self.board.add_disc(PINK, self.right_column + 1)

    def test_add_and_get_one_disc_left_column(self):
        self.board.add_disc(PINK, self.left_column)
        self.assertEqual(PINK, self.board.get_disc(self.bottom_left))
        self.assertIsNone(self.board.get_disc(self.bottom_right))

    def test_add_and_get_one_disc_right_column(self):
        self.board.add_disc(PINK, self.right_column)
        self.assertEqual(PINK, self.board.get_disc(self.bottom_right))
        self.assertIsNone(self.board.get_disc(self.bottom_left))


class TestMatchesAndWins(unittest.TestCase):

    def setUp(self):
        self.board = Board(TEST_NUM_ROWS, TEST_NUM_COLUMNS, TEST_NUM_TO_WIN)
        test_plays = (
            (BROWN, 1),
            (PINK, 2),
            (BROWN, 2),
            (PINK, 2),
            (BROWN, 2),
            (PINK, 3),
            (BROWN, 3),
            (PINK, 0),
            (BROWN, 3),
            (PINK, 4),
            (BROWN, 4),
            (PINK, 3),
            (BROWN, 4),
            (PINK, 4),
            (BROWN, 5),
        )

        for play in test_plays:
            self.board.add_disc(*play)

    def test_consecutive_matches(self):
        m = self.board._get_consecutive_matches((2, 2), (0, 1))
        self.assertEquals(m, {(2, 2), (2, 3), (2, 4)})

    def test_consecutive_matches_one_only(self):
        m = self.board._get_consecutive_matches((2, 2), (0, -1))
        self.assertEquals(m, {(2, 2)})

    def test_consecutive_matches_mirrored_both_dir_relevant(self):
        m = self.board._get_consecutive_matches_mirrored((2, 3), (0, 1))
        n = self.board._get_consecutive_matches_mirrored((2, 3), (0, -1))
        self.assertEquals(m, n)
        self.assertEquals(m, {(2, 2), (2, 3), (2, 4)})

    def test_consecutive_matches_mirrored_only_one_dir_relevant(self):
        m = self.board._get_consecutive_matches_mirrored((2, 2), (0, 1))
        n = self.board._get_consecutive_matches_mirrored((2, 2), (0, -1))
        self.assertEquals(m, n)
        self.assertEquals(m, {(2, 2), (2, 3), (2, 4)})

    def test_winning_positions_diagonal_both_dir_relevant(self):
        w = self.board.get_winning_positions((2, 4))
        self.assertEquals(w, {(0, 2), (1, 3), (2, 4), (3, 5)})

    def test_winning_positions_diagonal_only_one_dir_relevant(self):
        w = self.board.get_winning_positions((3, 5))
        self.assertEquals(w, {(0, 2), (1, 3), (2, 4), (3, 5)})

    def test_winning_positions_with_fake(self):
        w = self.board.get_winning_positions((2, 1), fake_disc=BROWN)
        self.assertEquals(w, {(2, 1), (2, 2), (2, 3), (2, 4)})
