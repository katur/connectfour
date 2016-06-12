import unittest

from connectfour.model.game import Game
from connectfour.util.color import Color

TEST_NUM_ROWS = 4
TEST_NUM_COLUMNS = 6
TEST_NUM_TO_WIN = 4


def create_game():
    c = Game()
    c.add_player('Sally', Color.brown)
    c.add_player('Fred', Color.pink)
    c.add_board(TEST_NUM_ROWS, TEST_NUM_COLUMNS, TEST_NUM_TO_WIN)
    return c


def make_plays(c):
    plays = [1, 2, 2, 2, 2, 3, 3, 0, 3, 4, 4, 3, 4, 4]
    for play in plays:
        c.play_disc(play)
    return c


class TestRoundNotStarted(unittest.TestCase):

    def setUp(self):
        self.c = create_game()

    def test_round_not_in_progress_at_beginning(self):
        self.assertFalse(self.c.round_in_progress)

    def test_get_num_players(self):
        self.assertEqual(self.c.get_num_players(), 2)

    def test_first_player_before_round_started(self):
        self.assertEqual(self.c.get_current_player().name, 'Sally')


class TestRoundStarted(unittest.TestCase):

    def setUp(self):
        self.c = create_game()
        self.c.start_round()

    def test_round_in_progress(self):
        self.assertTrue(self.c.round_in_progress)

    def test_first_player_after_round_started(self):
        self.assertEqual(self.c.get_current_player().name, 'Sally')


class TestRoundInProgress(unittest.TestCase):

    def setUp(self):
        self.c = create_game()
        self.c.start_round()
        make_plays(self.c)

    def test_current_player(self):
        self.assertEqual(self.c.get_current_player().name, 'Sally')


class TestRoundWon(unittest.TestCase):

    def setUp(self):
        self.c = create_game()
        self.c.start_round()
        make_plays(self.c)
        self.c.play_disc(5)

    def test_round_not_in_progress_after_round_won(self):
        self.assertFalse(self.c.round_in_progress)
