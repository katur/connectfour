from connectfour.model.game import Game
from connectfour.util.color import Color
from connectfour.views.logger import LogView


game = Game(num_rows=6, num_columns=7, num_to_win=4)
logger_view = LogView(game)

game.add_player('tim', Color.black)
game.add_player('xavier', Color.red)
game.start_round()
game.play_disc(0)
game.play_disc(1)
game.play_disc(1)
game.play_disc(4)
game.play_disc(2)
game.play_disc(4)
game.play_disc(2)
game.play_disc(4)
game.play_disc(2)
game.play_disc(4)
