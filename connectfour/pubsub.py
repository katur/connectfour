from enum import Enum
from collections import deque


class ModelAction(Enum):
    """An action that occurs in the game.

    These are the actions that the model publishes, and which views may
    subscribe to.
    """
    (
        player_added, player_removed, board_created, game_started,
        next_player, try_again, color_played, game_won, game_draw,
    ) = range(9)


class ViewAction(Enum):
    (
        add_player, remove_player, create_board, start_game, play,
        request_ai_play
    ) = range(6)


class PubSub(object):
    def __init__(self):
        # To store all subscribed callback functions, keyed on Action
        self.subscriptions = {}

        self.queue = deque()

    def do_queue(self):
        while len(self.queue):
            callback = self.queue.popleft()
            callback()

    def subscribe(self, action, callback):
        """Subscribe to a particular action.

        Args:
            action (Action): The action to subscribe to.
            callback (function): Will be called when action occurs.
        """
        if action not in self.subscriptions:
            self.subscriptions[action] = []

        self.subscriptions[action].append(callback)

    # TODO: add do_queue as arg to publish
    def publish(self, action, *args, **kwargs):
        """Publish that an action occurred.

        This calls any callbacks that are subscribed to the action.

        Args:
            action (Action): The action that occurred.
            *args: Will be passed to any subscribed callbacks.
            **kwargs: Will be passed to any subscribed callbacks.
        """
        if action not in self.subscriptions:
            return

        for callback in self.subscriptions[action]:
            def do_callback():
                return callback(*args, **kwargs)

            self.queue.append(do_callback)
