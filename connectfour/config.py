from enum import Enum

DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7
DEFAULT_TO_WIN = 4


class TryAgainReason(Enum):
    """Reason that a player needs to try again.

    A player needs to try again if their previous move was illegal.
    """

    column_out_of_bounds = 1
    column_full = 2


class Color(Enum):
    """A color to use for discs in the game.

    Yellow is not included because it should serve as the board background
    color, as in the real Connect Four game.
    """

    (black, red, blue, purple, brown, dark_green, pink, gray, orange,
        green) = range(10)


# List of all colors. May be used by a view to assign colors incrementally.
COLORS = [color for color in Color]
