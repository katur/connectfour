from enum import Enum


class Action(Enum):
    """An action that occurs in the game.

    These are the actions that the model publishes, and which the views
    may subscribe to.
    """
    player_added = 0
    board_created = 1
    round_started = 2
    next_player = 3
    try_again = 4
    disc_played = 5
    round_won = 6
    round_draw = 7


"""
Dictionary to store all subscribed callback functions, keyed on Action.
"""
subscriptions = {}


def subscribe(action, callback):
    """Subscribe to a particular action.

    Args:
        action (Action): The action to subscribe to.
        callback (function): Will be called when action occurs.
    """
    if action not in subscriptions:
        subscriptions[action] = []

    subscriptions[action].append(callback)


def publish(action, *args, **kwargs):
    """Publish that an action occurred.

    This results in any callbacks being called that are subscribed to
    the action.

    Args:
        action (Action): The action that occurred.
        *args, **kwargs: Will be passed to any subscribed callbacks.
    """
    if action not in subscriptions:
        return

    for callback in subscriptions[action]:
        callback(*args, **kwargs)
