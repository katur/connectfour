import unittest

from connectfour.config import Color
from connectfour.model import ConnectFourModel

TEST_ROWS = 4
TEST_COLUMNS = 6
TEST_TO_WIN = 4

ALICE = 'Alice'
BOB = 'Bob'

BROWN = Color.brown
GREEN = Color.green
PINK = Color.pink


def create_test_model():
    model = ConnectFourModel()
    model.add_player(ALICE, BROWN)
    model.add_player(BOB, PINK)
    model.create_board(TEST_ROWS, TEST_COLUMNS, TEST_TO_WIN)
    return model


FIRST_PLAY = 1
MORE_PLAYS = [2, 2, 2, 2, 3, 3, 0, 3, 4, 4, 3, 4, 4]
WINNING_PLAY = 5


class TestModelBeforeFirstGameStarted(unittest.TestCase):

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

    def test_get_remaining_colors(self):
        remaining = self.model.get_remaining_colors()
        self.assertNotIn(PINK, remaining)
        self.assertNotIn(BROWN, remaining)
        self.assertIn(GREEN, remaining)
        self.assertEqual(len(remaining), len(Color) - 2)


class TestModelWithoutBoardOrPlayers(unittest.TestCase):

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

    def test_get_remaining_colors_when_all_remaining(self):
        self.assertEqual(len(Color), len(self.model.get_remaining_colors()))


class TestModelAfterFirstGameStarted(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()

    def test_session_in_progress(self):
        self.assertTrue(self.model.session_in_progress)

    def test_game_in_progress(self):
        self.assertTrue(self.model.game_in_progress)

    def test_first_player_after_game_started(self):
        self.assertEqual(self.model.get_current_player().name, ALICE)


class TestModelAfterFirstPlay(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()
        self.model.play_disc(FIRST_PLAY)

    def test_current_player(self):
        self.assertEqual(self.model.get_current_player().name, BOB)


class TestModelGameInProgress(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()
        for play in [FIRST_PLAY] + MORE_PLAYS:
            self.model.play_disc(play)

    def test_current_player(self):
        self.assertEqual(self.model.get_current_player().name, ALICE)


class TestGameWon(unittest.TestCase):

    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()
        for play in [FIRST_PLAY] + MORE_PLAYS + [WINNING_PLAY]:
            self.model.play_disc(play)

    def test_game_not_in_progress_after_win(self):
        self.assertFalse(self.model.game_in_progress)

    def test_session_still_in_progress_after_win(self):
        self.assertTrue(self.model.session_in_progress)

    def test_win_recorded_in_player(self):
        alice = self.model.players[0]
        bob = self.model.players[1]
        if alice.name != ALICE:
            unittest.TestCase.fail('Alice should be index 0')
        if bob.name != BOB:
            unittest.TestCase.fail('Bob should be index 1')

        self.assertEqual(alice.num_wins, 1)
        self.assertEqual(bob.num_wins, 0)


class TestNextGameStarted(unittest.TestCase):
    def setUp(self):
        self.model = create_test_model()
        self.model.start_game()
        for play in [FIRST_PLAY] + MORE_PLAYS + [WINNING_PLAY]:
            self.model.play_disc(play)
        self.model.start_game()

    def test_game_in_progress_second_game(self):
        self.assertTrue(self.model.game_in_progress)

    def test_first_player_rotates(self):
        self.assertEqual(self.model.get_current_player().name, BOB)
