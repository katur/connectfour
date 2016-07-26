import argparse

from connectfour.model import ConnectFourModel
from connectfour.pubsub import PubSub
from connectfour.views.commandline.view import CommandLineView


parser = argparse.ArgumentParser(
    description='Play Connect Four from the command line.')

args = parser.parse_args()

pubsub = PubSub()
model = ConnectFourModel(pubsub)
view = CommandLineView(pubsub, model)
pubsub.do_queue()
