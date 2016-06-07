from model.board import Board
from model.disc import Disc

b = Board(4, 6)

print b.get_printable_grid()


pink = Disc('pink')
brown = Disc('brown')

b.add_disc(pink, 2)
b.add_disc(brown, 2)
b.add_disc(pink, 2)
b.add_disc(brown, 2)
b.add_disc(pink, 0)

print b.get_printable_grid()
