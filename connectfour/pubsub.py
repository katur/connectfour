from enum import Enum


class Action(Enum):
    player_added = 0
    round_started = 1
    next_player = 2
    try_again = 3
    disc_played = 4
    round_won = 5
    round_draw = 6


callbacks = {}


def subscribe(action, callback):
    if action not in callbacks:
        callbacks[action] = []

    callbacks[action].append(callback)


def publish(action, *args, **kwargs):
    if action not in callbacks:
        return

    for callback in callbacks[action]:
        callback(*args, **kwargs)
