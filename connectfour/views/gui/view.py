import Tkinter as tk

from connectfour import pubsub
from connectfour.util.color import COLORS

from config import WINDOW_TITLE_TEXT
from gameframe import GameFrame
from setupframe import SetupFrame


class GUIView(object):
    """Top-level GUI control."""

    def __init__(self, model):
        self.model = model
        self._create_subscriptions()

        # Initialize GUI window
        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE_TEXT)

        # Initialize and launch setup screen
        self.setup_frame = SetupFrame(self)
        self.window.mainloop()

    def _create_subscriptions(self):
        responses = {
            pubsub.Action.player_added: self.on_player_added,
            pubsub.Action.round_started: self.on_round_started,
            pubsub.Action.next_player: self.on_next_player,
            pubsub.Action.try_again: self.on_try_again,
            pubsub.Action.disc_played: self.on_disc_played,
            pubsub.Action.round_won: self.on_round_won,
            pubsub.Action.round_draw: self.on_round_draw,
        }

        for action, response in responses.iteritems():
            pubsub.subscribe(action, response)

    def quit(self):
        self.window.quit()

    ######################
    # Calls to the model #
    ######################

    def add_player(self):
        name = self.setup_frame.parse_player_entry()
        color = COLORS[self.model.get_num_players()]
        self.model.add_player(name, color)

    def launch_game(self):
        # Create the game board
        try:
            num_rows = self.setup_frame.parse_row_entry()
            num_columns = self.setup_frame.parse_column_entry()
            num_to_win = self.setup_frame.parse_to_win_entry()
            self.model.add_board(num_rows, num_columns, num_to_win)

        except ValueError:
            # TODO: handle erroneous row/column/to_win
            return

        # Move on to game frame
        self.setup_frame.remove()
        self.game_frame = GameFrame(self, num_rows, num_columns)
        self.model.start_round()

    def play_again(self):
        self.game_frame.reset_squares()
        self.model.start_round()

    def play_disc(self, column):
        self.model.play_disc(column)

    ###########################
    # Respond to model events #
    ###########################

    def on_player_added(self, player):
        self.setup_frame.update_player_feedback(
            player, self.model.get_num_players())

        # Enable launch once first player is added
        self.setup_frame.enable_launch_button()

    def on_round_started(self, round_number):
        self.game_frame.disable_play_again_button()
        self.game_frame.enable_column_buttons()

    def on_next_player(self, player):
        self.game_frame.announce_next_player(player)

    def on_try_again(self, player, reason):
        self.game_frame.announce_try_again(player, reason)

    def on_disc_played(self, player, position):
        self.game_frame.update_square(player, position)

    def on_round_won(self, player, winning_positions):
        self.game_frame.announce_winner(player)
        self.game_frame.disable_column_buttons()
        self.game_frame.enable_play_again_button()
        self.game_frame.flash_squares(winning_positions)

    def on_round_draw(self):
        self.game_frame.announce_draw()
        self.game_frame.disable_column_buttons()
        self.game_frame.enable_play_again_button()
