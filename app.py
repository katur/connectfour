from connectfour.model.game import Game
from connectfour.views.gui.view import GUIView
from connectfour.views.logger.view import LogView


game = Game()

log_view = LogView()
gui_view = GUIView(model=game)
