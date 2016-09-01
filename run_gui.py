#!/usr/bin/env python

import argparse

from connectfour.model import ConnectFourModel
from connectfour.pubsub import PubSub
from connectfour.gui.view import GUIView
from connectfour.logger.view import LogView


parser = argparse.ArgumentParser(
    description='Play Connect Four with a GUI.')

parser.add_argument('--log', dest='log', action='store_true',
                    help='Log actions to the console')

args = parser.parse_args()

pubsub = PubSub()
model = ConnectFourModel(pubsub)

if args.log:
    log_view = LogView(pubsub)

gui_view = GUIView(pubsub, model)
