import unittest

from connectfour.model import Color, Player

ALICE = 'Alice'
RED = Color.red


#####################
# Test Player class #
#####################

class TestPlayer_Basics(unittest.TestCase):

    def setUp(self):
        self.alice = Player(ALICE, RED)

    def test_name(self):
        self.assertEqual(self.alice.name, ALICE)

    def test_color(self):
        self.assertEqual(self.alice.color, RED)

    def test_num_wins(self):
        self.assertEqual(self.alice.num_wins, 0)
