import unittest
import string

from connectfour.model import Board, Color, ConnectFourModel, Player

TEST_ROWS = 4
TEST_COLUMNS = 6
TEST_TO_WIN = 4

ALICE = 'Alice'
BOB = 'Bob'

BROWN = Color.brown
GREEN = Color.green
ORANGE = Color.orange
PINK = Color.pink


####################
# Test Board class #
####################

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
        self.board.add_color(PINK, self.left_column)
        self.assertEqual(PINK, self.board.get_color(self.bottom_left))
        self.assertIsNone(self.board.get_color(self.bottom_right))

    def test_add_and_get_one_color_right_column(self):
        self.board.add_color(PINK, self.right_column)
        self.assertEqual(PINK, self.board.get_color(self.bottom_right))
        self.assertIsNone(self.board.get_color(self.bottom_left))

    def test_add_color_out_of_bounds_left(self):
        with self.assertRaises(ValueError):
            self.board.add_color(PINK, self.left_column - 1)

    def test_add_color_out_of_bounds_right(self):
        with self.assertRaises(ValueError):
            self.board.add_color(PINK, self.right_column + 1)

    def test_is_column_full_when_empty(self):
        self.assertFalse(self.board.is_column_full(self.left_column))

    def test_is_column_full_when_only_one(self):
        self.board.add_color(PINK, self.left_column)
        self.assertFalse(self.board.is_column_full(self.left_column))

    def test_is_column_full_when_missing_one(self):
        for i in range(self.board.num_rows - 1):
            self.board.add_color(PINK, self.left_column)
        self.assertFalse(self.board.is_column_full(self.left_column))

    def test_is_column_full_when_full(self):
        for i in range(self.board.num_rows):
            self.board.add_color(PINK, self.left_column)
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
        self.board.add_color(PINK, self.left_column)
        self.assertFalse(self.board.is_full())

    def test_is_board_full_when_missing_one(self):
        # Fill entire board except last column
        for column in range(self.board.num_columns - 1):
            for row in range(self.board.num_rows):
                self.board.add_color(PINK, column)

        # Fill last column except for top row
        for row in range(self.board.num_rows - 1):
            self.board.add_color(PINK, self.right_column)

        self.assertFalse(self.board.is_full())

    def test_is_board_full_when_full(self):
        self._fill_board()
        self.assertTrue(self.board.is_full())

    def test_reset_empty_board(self):
        self.assertTrue(self._is_empty())
        self.board.reset()
        self.assertTrue(self._is_empty())

    def test_reset_partial_board(self):
        # Fill left and right columns (to get all corners)
        for row in range(self.board.num_rows):
            self.board.add_color(PINK, self.left_column)
            self.board.add_color(PINK, self.right_column)

        self.assertFalse(self._is_empty())
        self.board.reset()
        self.assertTrue(self._is_empty())

    def test_reset_full_board(self):
        self._fill_board()
        self.assertFalse(self._is_empty())
        self.board.reset()
        self.assertTrue(self._is_empty())

    ###########
    # Helpers #
    ###########

    def _is_empty(self):
        for row in range(self.board.num_rows):
            for column in range(self.board.num_columns):
                if self.board.grid[row][column]:
                    return False
        return True

    def _fill_board(self):
        for column in range(self.board.num_columns):
            for row in range(self.board.num_rows):
                self.board.add_color(PINK, column)


BOARD_PLAYS = (
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


class TestBoard_MatchesAndWins(unittest.TestCase):

    def setUp(self):
        self.board = Board(TEST_ROWS, TEST_COLUMNS, TEST_TO_WIN)

        for play in BOARD_PLAYS:
            self.board.add_color(*play)

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
        w = self.board.get_winning_positions((2, 1), fake_color=BROWN)
        self.assertEquals(w, {(2, 1), (2, 2), (2, 3), (2, 4)})


#####################
# Test Player class #
#####################

class TestPlayer_Basics(unittest.TestCase):

    def setUp(self):
        self.alice = Player(ALICE, ORANGE)

    def test_name(self):
        self.assertEqual(self.alice.name, ALICE)

    def test_color(self):
        self.assertEqual(self.alice.color, ORANGE)

    def test_num_wins(self):
        self.assertEqual(self.alice.num_wins, 0)


###############################
# Test ConnectFourModel class #
###############################

MODEL_PLAYS = [1, 2, 2, 2, 2, 3, 3, 0, 3, 4, 4, 3, 4, 4, 5]


class TestModel_EmptyModel(unittest.TestCase):

    def setUp(self):
        self.model = ConnectFourModel()

    def test_get_num_rows_when_no_board(self):
        self.assertIsNone(self.model.get_num_rows())

    def test_get_num_columns_when_no_board(self):
        self.assertIsNone(self.model.get_num_columns())

    def test_get_num_to_win_when_no_board(self):
        self.assertIsNone(self.model.get_num_to_win())

    def test_get_num_players_when_none(self):
        self.assertEqual(self.model.get_num_players(), 0)

    def test_get_current_player_when_none(self):
        self.assertIsNone(self.model.get_current_player())

    def test_used_colors_when_none(self):
        self.assertEqual(len(self.model.used_colors), 0)

    def test_add_max_players(self):
        num = len(Color)
        for index, name in enumerate(string.ascii_lowercase[:num]):
            self.model.add_player(name, Color(index))

        self.assertEqual(len(self.model.used_colors), num)
        self.assertEqual(self.model.get_num_players(), num)


def create_test_model():
    model = ConnectFourModel()
    model.add_player(ALICE, BROWN)
    model.add_player(BOB, PINK)
    model.create_board(TEST_ROWS, TEST_COLUMNS, TEST_TO_WIN)
    return model


class TestModel_BeforeFirstGameStarted(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()

    def test_session_in_progress_before_first_game(self):
        self.assertFalse(self.model.session_in_progress)

    def test_game_in_progress_before_first_game(self):
        self.assertFalse(self.model.game_in_progress)

    def test_game_number_before_first_game(self):
        self.assertEqual(self.model.game_number, 0)

    def test_get_num_rows(self):
        self.assertEqual(self.model.get_num_rows(), TEST_ROWS)

    def test_get_num_columns(self):
        self.assertEqual(self.model.get_num_columns(), TEST_COLUMNS)

    def test_get_num_to_win(self):
        self.assertEqual(self.model.get_num_to_win(), TEST_TO_WIN)

    def test_get_num_players(self):
        self.assertEqual(self.model.get_num_players(), 2)

    def test_get_current_player_before_first_game(self):
        self.assertEqual(self.model.get_current_player().name, ALICE)

    def test_used_colors(self):
        self.assertEqual(self.model.used_colors, {PINK, BROWN})


class TestModel_AfterFirstGameStarted(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()

    def test_session_in_progress(self):
        self.assertTrue(self.model.session_in_progress)

    def test_game_in_progress(self):
        self.assertTrue(self.model.game_in_progress)

    def test_first_player_after_game_started(self):
        self.assertEqual(self.model.get_current_player().name, ALICE)


class TestModel_AfterFirstPlay(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()
        self.model.play(MODEL_PLAYS[0])

    def test_current_player(self):
        self.assertEqual(self.model.get_current_player().name, BOB)


class TestModel_GameInProgress(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()
        for column in MODEL_PLAYS[:-1]:
            self.model.play(column)

    def test_current_player(self):
        self.assertEqual(self.model.get_current_player().name, ALICE)


class TestModel_GameWon(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()
        for column in MODEL_PLAYS:
            self.model.play(column)

    def test_game_not_in_progress_after_win(self):
        self.assertFalse(self.model.game_in_progress)

    def test_session_still_in_progress_after_win(self):
        self.assertTrue(self.model.session_in_progress)

    def test_win_recorded_in_player(self):
        alice = self.model.get_player(0)
        bob = self.model.get_player(1)
        if alice.name != ALICE:
            unittest.TestCase.fail('Alice should be index 0')
        if bob.name != BOB:
            unittest.TestCase.fail('Bob should be index 1')

        self.assertEqual(alice.num_wins, 1)
        self.assertEqual(bob.num_wins, 0)


class TestModel_NextGameStarted(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()
        for column in MODEL_PLAYS:
            self.model.play(column)
        self.model.start_game()

    def test_game_in_progress_second_game(self):
        self.assertTrue(self.model.game_in_progress)

    def test_first_player_rotates(self):
        self.assertEqual(self.model.get_current_player().name, BOB)
