import Disc


class Player(object):
    """
    A Connect Four player.
    """
    def __init__(self, name, color, order):
        self.name = name

        # TODO: set this automatically with a class-level variable
        self.order = order
        self.disc = Disc(color=color)
        self.number_of_wins = 0

    def __str__(self):
        return '{} ()'.format(self.name, self.color)

    def __repr__(self):
        return self.__str__()
