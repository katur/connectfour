class Disc(object):
    """
    A Connect Four playing disc (aka token, or chip).

    TODO: consider a factory design pattern so that each player uses only
    one chip object.
    """

    def __init__(self, color):
        self.color = color

    def __str__(self):
        return '{} Disc'.format(self.color)

    def __repr__(self):
        return self.__str__()
