from connectfour.model.board import Board
from connectfour.model.disc import Disc

b = Board(4, 6)

print b.get_printable_grid()


pink = Disc('pink')
brown = Disc('brown')

b.add_disc(brown, 1)

b.add_disc(pink, 2)
b.add_disc(brown, 2)
b.add_disc(pink, 2)
b.add_disc(brown, 2)

b.add_disc(pink, 3)
b.add_disc(brown, 3)
b.add_disc(brown, 3)
b.add_disc(pink, 3)

b.add_disc(pink, 4)
b.add_disc(brown, 4)
b.add_disc(brown, 4)
b.add_disc(pink, 4)


print b.get_printable_grid()

print b.get_num_outward_discs_1D(brown, (2, 2), (0, 1))
print b.get_num_outward_discs_1D(brown, (2, 2), (0, -1))
print b.get_num_outward_discs_2D(brown, (2, 2), (0, 1))

print b.check_for_win(brown, (2, 1), 4)
print b.check_for_win(brown, (3, 5), 5)
