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

print 'Browns up from [2,2]: {}'.format(
    b.get_consecutive_matches(brown, (2, 2), (0, 1)))

print 'Browns down from [2,2]: {}'.format(
    b.get_consecutive_matches(brown, (2, 2), (0, -1)))

print 'Browns up/down from [2,2]: {}'.format(
    b.get_consecutive_matches_mirrored(brown, (2, 2), (0, 1)))

print 'Winning 4-positions with fake brown at [2,1]: {}'.format(
    b.get_winning_positions((2, 1), 4, fake_disc=brown))

print 'Winning 4-positions with fake brown at [3,5]: {}'.format(
    b.get_winning_positions((3, 5), 4, fake_disc=brown))
