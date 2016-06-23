import argparse

from model import ConnectFourModel
from view import CommandLineView


parser = argparse.ArgumentParser(
    description='Play Connect Four from the command line.')

args = parser.parse_args()

model = ConnectFourModel()
view = CommandLineView(model)
