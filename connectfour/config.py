from enum import Enum


class TryAgainReason(Enum):
    """Reason that a player needs to try again.

    They need to try again if their previous move was illegal.
    """

    column_out_of_bounds = 1
    column_full = 2


class Color(Enum):
    """A color."""

    (black, red, blue, purple, brown, dark_green, pink, gray, orange,
        green) = range(10)


def get_color_dictionary():
    """Get a dictionary mapping integers to colors."""
    colors = {}

    for color in Color:
        colors[color.value] = color

    return colors


COLORS = [color for color in Color]
