from connectfour.model.model import ConnectFourModel
from connectfour.views.gui.view import GUIView
from connectfour.views.logger.view import LogView


model = ConnectFourModel()
log_view = LogView()
gui_view = GUIView(model)
