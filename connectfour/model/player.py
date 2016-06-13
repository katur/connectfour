from connectfour.model.disc import Disc


class Player(object):
    """A Connect Four player."""

    def __init__(self, name, color):
        self.name = name
        self.disc = Disc(color)
        self.number_of_wins = 0

    def __str__(self):
        return '{} ({})'.format(self.name, self.disc.color.name)

    def __repr__(self):
        return self.__str__()

    def get_color(self):
        """Get this player's disc color."""
        return self.disc.color
