from connectfour.model.board import Board
from connectfour.model.disc import Disc

b = Board(num_rows=4, num_columns=6, num_to_win=4)

pink = Disc('pink')
brown = Disc('brown')

b.add_disc(brown, 1)
b.add_disc(pink, 2)
b.add_disc(brown, 2)
b.add_disc(pink, 2)
b.add_disc(brown, 2)
b.add_disc(pink, 3)
b.add_disc(brown, 3)
b.add_disc(pink, 0)
b.add_disc(brown, 3)
b.add_disc(pink, 4)
b.add_disc(brown, 4)
b.add_disc(pink, 3)
b.add_disc(brown, 4)
b.add_disc(pink, 4)
b.add_disc(brown, 5)

print b.get_printable_grid()

print 'Matches right from (2, 2): {}'.format(
    b.get_consecutive_matches((2, 2), (0, 1)))

print 'Matches left from (2, 2): {}'.format(
    b.get_consecutive_matches((2, 2), (0, -1)))

print 'Matches right/left from (2, 2): {}'.format(
    b.get_consecutive_matches_mirrored((2, 2), (0, 1)))

print 'Winning 4-positions from (3, 5): {}'.format(
    b.get_winning_positions((3, 5)))

print 'Winning 4-positions from (2, 4): {}'.format(
    b.get_winning_positions((3, 5)))

print 'Winning 4-positions with fake brown from (2, 1): {}'.format(
    b.get_winning_positions((2, 1), fake_disc=brown))
