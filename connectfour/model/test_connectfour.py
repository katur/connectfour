import unittest

from color import Color
from connectfour import ConnectFour

TEST_NUM_ROWS = 4
TEST_NUM_COLUMNS = 6
TEST_NUM_TO_WIN = 4


def create_game():
    c = ConnectFour(TEST_NUM_ROWS, TEST_NUM_COLUMNS, TEST_NUM_TO_WIN)
    c.add_player('Sally', Color.brown)
    c.add_player('Fred', Color.pink)
    return c


def populate_game(c):
    plays = [1, 2, 2, 2, 2, 3, 3, 0, 3, 4, 4, 3, 4, 4]
    for play in plays:
        c.play_disc(play)
    return c


class TestGameNotYetStarted(unittest.TestCase):

    def setUp(self):
        self.c = create_game()

    def test_game_not_started_yet(self):
        self.assertFalse(self.c.game_in_progress)

    def test_get_num_players(self):
        self.assertEqual(self.c.get_num_players(), 2)

    def test_first_player(self):
        self.assertEqual(self.c.get_current_player().name, 'Sally')


class TestGameStarted(unittest.TestCase):

    def setUp(self):
        self.c = create_game()
        self.c.start_game()

    def test_game_in_progress(self):
        self.assertTrue(self.c.game_in_progress)

    def test_first_player(self):
        self.assertEqual(self.c.get_current_player().name, 'Sally')


class TestGameInProgress(unittest.TestCase):

    def setUp(self):
        self.c = create_game()
        self.c.start_game()
        populate_game(self.c)

    def test_current_player(self):
        self.assertEqual(self.c.get_current_player().name, 'Sally')


class TestGameWon(unittest.TestCase):

    def setUp(self):
        self.c = create_game()
        self.c.start_game()
        populate_game(self.c)
        self.c.play_disc(5)

    def test_game_no_longer_in_progress(self):
        self.assertFalse(self.c.game_in_progress)
