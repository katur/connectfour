import unittest

from connectfour.config import Color
from connectfour.model import Player

ALICE = 'Alice'
ORANGE = Color.orange


class TestPlayerBasics(unittest.TestCase):

    def setUp(self):
        self.alice = Player(ALICE, ORANGE)

    def test_name(self):
        self.assertEqual(self.alice.name, ALICE)

    def test_color(self):
        self.assertEqual(self.alice.color, ORANGE)

    def test_num_wins(self):
        self.assertEqual(self.alice.num_wins, 0)
