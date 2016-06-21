import unittest

from connectfour.config import Color
from connectfour.model import Disc

GREEN = Color.green
ORANGE = Color.orange


class TestDiscBasics(unittest.TestCase):

    def setUp(self):
        self.orange_disc = Disc(ORANGE)

    def test_color(self):
        self.assertEqual(self.orange_disc.color, ORANGE)

    def test_equals(self):
        other = Disc(ORANGE)
        self.assertEqual(self.orange_disc, other)

    def test_not_equal(self):
        other = Disc(GREEN)
        self.assertNotEqual(self.orange_disc, other)
