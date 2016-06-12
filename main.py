from connectfour.model.game import Game
from connectfour.views.gui import GUIView
from connectfour.views.logger import LogView


game = Game()

log_view = LogView(game)
gui_view = GUIView(game)
