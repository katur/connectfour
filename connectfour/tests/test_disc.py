import unittest

from connectfour.config import ConnectFourColor
from connectfour.model import ConnectFourDisc

GREEN = ConnectFourColor.green
ORANGE = ConnectFourColor.orange


class TestDiscBasics(unittest.TestCase):

    def setUp(self):
        self.orange_disc = ConnectFourDisc(ORANGE)

    def test_color(self):
        self.assertEqual(self.orange_disc.color, ORANGE)

    def test_equals(self):
        other = ConnectFourDisc(ORANGE)
        self.assertEqual(self.orange_disc, other)

    def test_not_equal(self):
        other = ConnectFourDisc(GREEN)
        self.assertNotEqual(self.orange_disc, other)
