import argparse

from connectfour.model import ConnectFourModel
from connectfour.views.commandline.view import CommandLineView


parser = argparse.ArgumentParser(
    description='Play Connect Four from the command line.')

args = parser.parse_args()

model = ConnectFourModel()
view = CommandLineView(model)
