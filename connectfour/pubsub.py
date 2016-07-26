from enum import Enum
from collections import deque


class ModelAction(Enum):
    """An action that occurs in the game.

    These are the actions that the model publishes, and which views may
    subscribe to.
    """
    player_added = 0
    board_created = 1
    game_started = 2
    next_player = 3
    try_again = 4
    color_played = 5
    game_won = 6
    game_draw = 7


class ViewAction(Enum):
    add_player = 0
    create_board = 1
    start_game = 2
    play = 3
    request_ai_play = 4


subscriptions = {}
"""dict: To store all subscribed callback functions, keyed on Action."""

queue = deque()


def do_queue():
    while len(queue):
        callback = queue.popleft()
        callback()


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

    This calls any callbacks that are subscribed to the action.

    Args:
        action (Action): The action that occurred.
        *args: Will be passed to any subscribed callbacks.
        **kwargs: Will be passed to any subscribed callbacks.
    """
    if action not in subscriptions:
        return

    for callback in subscriptions[action]:
        def do_callback():
            return callback(*args, **kwargs)

        queue.append(do_callback)
