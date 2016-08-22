import unittest
import string

from connectfour.pubsub import PubSub
from connectfour.model import Color, ConnectFourModel

TEST_ROWS = 6
TEST_COLUMNS = 7
TEST_TO_WIN = 4

P0_NAME = 'Alice'
P1_NAME = 'Bob'
P2_NAME = 'Carol'

P0_COLOR = Color.pink
P1_COLOR = Color.blue
P2_COLOR = Color.gray

PLAYS = {
    '2P-1W': [1, 2, 2, 2, 2, 3, 3, 0, 3, 4, 4, 3, 4, 4, 6, 6, 5],
}
"""Test plays for a board with TEST_ROWS, TEST_COLUMNS, TEST_TO_WIN.

2P-1W (2-player game, 1st player wins) looks like:


                    pink    blue    blue
                    blue    pink    pink
                    pink    pink    pink            blue
    blue    pink    blue    blue    blue    pink    pink
"""


def create_two_player_model():
    model = ConnectFourModel(PubSub())
    model._add_player(P0_NAME, P0_COLOR)
    model._add_player(P1_NAME, P1_COLOR)
    model._create_board(TEST_ROWS, TEST_COLUMNS, TEST_TO_WIN)
    return model


class TestModel_EmptyModel(unittest.TestCase):

    def setUp(self):
        self.model = ConnectFourModel(PubSub())

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
            self.model._add_player(name, Color(index))

        self.assertEqual(len(self.model.used_colors), num)
        self.assertEqual(self.model.get_num_players(), num)


class TestModel_BeforeFirstGameStarted(unittest.TestCase):

    def setUp(self):
        self.model = create_two_player_model()

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

    def test_current_player(self):
        self.assertEqual(self.model.get_current_player().name, P0_NAME)

    def test_used_colors(self):
        self.assertEqual(self.model.used_colors, {P1_COLOR, P0_COLOR})


class TestModel_FirstGameStarted(unittest.TestCase):

    def setUp(self):
        self.model = create_two_player_model()
        self.model._start_game()

    def test_game_in_progress(self):
        self.assertTrue(self.model.game_in_progress)

    def test_current_player(self):
        self.assertEqual(self.model.get_current_player().name, P0_NAME)


class TestModel_FirstPlayMade(unittest.TestCase):

    def setUp(self):
        self.model = create_two_player_model()
        self.model._start_game()
        self.model._play(PLAYS['2P-1W'][0])

    def test_current_player(self):
        self.assertEqual(self.model.get_current_player().name, P1_NAME)


class TestModel_OnePlayBeforeWin(unittest.TestCase):

    def setUp(self):
        self.model = create_two_player_model()
        self.model._start_game()
        for column in PLAYS['2P-1W'][:-1]:
            self.model._play(column)

    def test_current_player(self):
        self.assertEqual(self.model.get_current_player().name, P0_NAME)

    def test_game_in_progress(self):
        self.assertTrue(self.model.game_in_progress)


class TestModel_GameWon(unittest.TestCase):

    def setUp(self):
        self.model = create_two_player_model()
        self.model._start_game()
        for column in PLAYS['2P-1W']:
            self.model._play(column)

    def test_game_not_in_progress_after_win(self):
        self.assertFalse(self.model.game_in_progress)

    def test_win_recorded_in_player(self):
        p0 = self.model.get_player(0)
        p1 = self.model.get_player(1)

        self.assertEqual(p0.num_wins, 1)
        self.assertEqual(p1.num_wins, 0)


class TestModel_SecondGameStarted(unittest.TestCase):

    def setUp(self):
        self.model = create_two_player_model()
        self.model._start_game()
        for column in PLAYS['2P-1W']:
            self.model._play(column)
        self.model._start_game()

    def test_game_in_progress_second_game(self):
        self.assertTrue(self.model.game_in_progress)

    def test_first_player_rotates(self):
        self.assertEqual(self.model.get_current_player().name, P1_NAME)
