from connectfour.model.game import ConnectFour

c = ConnectFour(num_rows=4, num_columns=6, num_to_win=4)
c.add_player('Sally', 'brown')
c.add_player('Fred', 'pink')

c.start_game()

c.play_disc(1)
c.play_disc(2)
c.play_disc(2)
c.play_disc(2)
c.play_disc(2)
c.play_disc(3)
c.play_disc(3)
c.play_disc(0)
c.play_disc(3)
c.play_disc(4)
c.play_disc(4)
c.play_disc(3)
c.play_disc(4)
c.play_disc(4)
c.play_disc(5)

print c.board.get_printable_grid()

c.start_game()
c.play_disc(4)
print c.board.get_printable_grid()
