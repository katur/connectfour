class Disc(object):
    """A Connect Four playing disc (aka token, or chip).

    Each player creates just one disc, and plays the same disc repeatedly
    in different positions.
    """

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return '{}'.format(self.color)

    def __repr__(self):
        return '{} Disc'.format(self.color)
