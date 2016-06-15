from connectfour.model.disc import ConnectFourDisc


class ConnectFourPlayer(object):
    """A Connect Four player."""

    def __init__(self, name, color):
        """Create a player.

        Args:
            name (str): This player's name.
            color (ConnectFourColor): The color of this player's discs.
        """
        self.name = name
        self.disc = ConnectFourDisc(color)
        self.number_of_wins = 0

    def __str__(self):
        return '{} ({})'.format(self.name, self.disc.color.name)

    def __repr__(self):
        return self.__str__()

    def get_color(self):
        """Get this player's disc color.

        Returns:
            ConnectFourColor: The color of this player's discs.
        """
        return self.disc.color
