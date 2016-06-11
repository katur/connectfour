from enum import Enum


class TryAgainReason(Enum):
    """Reason that a player needs to try again.

    They need to try again if their previous move was illegal.
    """

    column_out_of_bounds = 1
    column_full = 2
