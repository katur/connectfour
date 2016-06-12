from enum import Enum


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
