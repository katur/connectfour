import argparse

from connectfour.model import ConnectFourModel
from connectfour.views.gui.view import GUIView
from connectfour.views.logger.view import LogView


parser = argparse.ArgumentParser(
    description='Play Connect Four with a GUI.')

parser.add_argument('--log', dest='log', action='store_true',
                    help='Log actions to the console')

args = parser.parse_args()

model = ConnectFourModel()

if args.log:
    log_view = LogView()

gui_view = GUIView(model)
