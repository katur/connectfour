from enum import Enum


class Color(Enum):
    """A disc color."""

    black = 0
    red = 1
    yellow = 2
    blue = 3
    orange = 4
    green = 5
    purple = 6
    pink = 7
    light_green = 8
    brown = 9


def get_color_dictionary():
    colors = {}

    for color in Color:
        colors[color.value] = color

    return colors


def get_color_list():
    return [color for color in Color]
