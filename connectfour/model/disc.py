class Disc(object):
    """
    A Connect Four playing disc (aka token, or chip).

    TODO: consider a factory design pattern so that each player instantiates
    only one chip object.
    """

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return '{}'.format(self.color)

    def __repr__(self):
        return '{} Disc'.format(self.color)
