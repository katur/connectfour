import argparse

from connectfour.model import ConnectFourModel
from connectfour.views.commandline.view import CommandLineView
from connectfour import pubsub


parser = argparse.ArgumentParser(
    description='Play Connect Four from the command line.')

args = parser.parse_args()

model = ConnectFourModel()
view = CommandLineView(model)
pubsub.trigger()
