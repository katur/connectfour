from connectfour.model.game import Game
from connectfour.views.gui import GUIView
from connectfour.views.logger import LogView


game = Game(num_rows=6, num_columns=7, num_to_win=4)

log_view = LogView(game)
gui_view = GUIView(game)
