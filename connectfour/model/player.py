from connectfour.model.disc import Disc


class Player(object):
    """A Connect Four player."""

    def __init__(self, name, color):
        """Create a player.

        Args:
            name (str): This player's name.
            color (Color): The color of this player's disc.
        """
        self.name = name
        self.disc = Disc(color)
        self.number_of_wins = 0

    def __str__(self):
        return '{} ({})'.format(self.name, self.disc.color.name)

    def __repr__(self):
        return self.__str__()

    def get_color(self):
        """Get the color of this player's disc.

        Returns:
            Color: The color of this player's disc.
        """
        return self.disc.color
