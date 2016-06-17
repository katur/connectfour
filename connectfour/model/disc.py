class ConnectFourDisc(object):
    """A Connect Four playing disc (aka token, or chip).

    Two discs are considered equal if they are the same color.
    """

    def __init__(self, color):
        """Create a disc.

        Args:
            color (ConnectFourColor): This disc's color.
        """
        self.color = color

    def __str__(self):
        return '{}'.format(self.color.name)

    def __repr__(self):
        return '{} ConnectFourDisc'.format(self.color)

    def __eq__(self, other):
        return type(other) is type(self) and self.color == other.color

    def __ne__(self, other):
        return not self.__eq__(other)
