from connectfour.model.model import ConnectFourModel
from connectfour.views.gui.view import GUIView
from connectfour.views.logger.view import LogView


model = ConnectFourModel()
gui_view = GUIView(model)
log_view = LogView()
