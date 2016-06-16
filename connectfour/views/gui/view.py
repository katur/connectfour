import Tkinter as tk
import tkMessageBox

from connectfour.config import COLORS
from connectfour.pubsub import subscribe, Action
from connectfour.views.gui.config import (
    WINDOW_TITLE, MAX_NAME_LENGTH, MAX_ROWS, MAX_COLUMNS, MAX_TO_WIN)
from connectfour.views.gui.gameframe import GameFrame
from connectfour.views.gui.setupframe import SetupFrame
from connectfour.views.gui.util import get_positive_int


class GUIView(object):
    """Tkinter GUI View of the Connect Four game."""

    def __init__(self, model):
        """Create this view, launching a Tkinter GUI in a new window.

        Args:
            model (ConnectFourModel): The model that this view will
                interact with.
        """
        self.model = model
        self._create_subscriptions()

        # Initialize GUI window
        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)

        # Initialize and launch setup screen
        self.setup_frame = SetupFrame(self)
        self.window.mainloop()

    def _create_subscriptions(self):
        responses = {
            Action.player_added: self.on_player_added,
            Action.round_started: self.on_round_started,
            Action.next_player: self.on_next_player,
            Action.try_again: self.on_try_again,
            Action.disc_played: self.on_disc_played,
            Action.round_won: self.on_round_won,
            Action.round_draw: self.on_round_draw,
        }

        for action, response in responses.iteritems():
            subscribe(action, response)

    def quit(self):
        """Quit the game."""
        self.window.quit()

    ######################
    # Calls to the model #
    ######################

    def add_player(self):
        """Tell the model to add a player.

        This method parses player attributes from user input. If input is
        invalid, a popup appears alerting the user to fix the error.
        """
        name = self.setup_frame.parse_player_entry()
        if not len(name):
            tkMessageBox.showerror('Error', 'Name must be non-empty')
            return

        if len(name) > MAX_NAME_LENGTH:
            tkMessageBox.showerror(
                'Error', "Name can't exceed {} characters"
                .format(MAX_NAME_LENGTH))
            return

        color = COLORS[self.model.get_num_players()]
        self.model.add_player(name, color)

    def launch_game(self):
        """Tell the model to create the board and start the first game.

        This method parses board parameters from user input. If input is
        invalid, a popup appears alerting the user to fix the error.

        This method also transitions the window from the setup_frame to the
        game_frame.
        """
        # Create the board
        try:
            self._create_board()
        except ValueError as e:
            tkMessageBox.showerror('Error', e)
            return

        # Move on to game frame
        self.setup_frame.remove()
        self.game_frame = GameFrame(self)
        self.model.start_round()

    def _create_board(self):
        num_rows = get_positive_int(
            self.setup_frame.parse_row_entry(),
            name='Rows', max_value=MAX_ROWS)
        num_columns = get_positive_int(
            self.setup_frame.parse_column_entry(),
            name='Columns', max_value=MAX_COLUMNS)
        num_to_win = get_positive_int(
            self.setup_frame.parse_to_win_entry(),
            name='To Win', max_value=MAX_TO_WIN)

        self.model.create_board(num_rows, num_columns, num_to_win)

    def play_again(self):
        """Tell the model to start a new game.

        This method also clears the game squares for the new game.
        """
        self.game_frame.reset_squares()
        self.model.start_round()

    def play_disc(self, column):
        """Tell the model that a disc was played in a column.

        The disc is assumed to be played by the current player.

        Args:
            column (int): The column to play the disc in.
        """
        self.model.play_disc(column)

    ###########################
    # Respond to model events #
    ###########################

    def on_player_added(self, player):
        """Respond to the model reporting that a player was added to the game.

        Args:
            player (ConnectFourPlayer): The player that was added.
        """
        self.setup_frame.update_feedback(player, self.model.get_num_players())

        # Enable launch once first player is added
        self.setup_frame.enable_launch_button()

    def on_round_started(self, round_number):
        """Respond to the model reporting that a new round started.

        Args:
            round_number (int): The number of the round that started.
        """
        self.game_frame.disable_play_again_button()
        self.game_frame.enable_play_buttons()

    def on_next_player(self, player):
        """Respond to the model reporting the next player.

        Args:
            player (ConnectFourPlayer): The player who should play next.
        """
        self.game_frame.announce_next_player(player)

    def on_try_again(self, player, reason):
        """Respond to the model reporting a try again event.

        Args:
            player (ConnectFourPlayer): The player who should try again.
            reason (TryAgainReason): The reason the player should try again.
        """
        self.game_frame.announce_try_again(player, reason)

    def on_disc_played(self, player, position):
        """Respond to the model reporting that a disc was played.

        Args:
            player (ConnectFourPlayer): The player who played the disc.
            position: A 2-tuple in format (row, column) of the position the
                disc was played.
        """
        self.game_frame.update_square(player, position)

    def on_round_won(self, player, winning_positions):
        """Respond to the model reporting that a round was won.

        Args:
            player (ConnectFourPlayer): The winner.
            winning_positions: The positions that resulted in the win.
        """
        self.game_frame.announce_win(player)
        self.game_frame.disable_play_buttons()
        self.game_frame.enable_play_again_button()
        self.game_frame.flash_squares(winning_positions)

    def on_round_draw(self):
        """Respond to the model reporting that a round ended in a draw."""
        self.game_frame.announce_draw()
        self.game_frame.disable_play_buttons()
        self.game_frame.enable_play_again_button()
