import Tkinter as tk

from connectfour.views.gui.config import (
    COLOR_TO_TK, REASON_TO_STR, GAME_TEXT, SQUARE_BACKGROUND, SQUARE_SIZE,
    SQUARE_BORDER_WIDTH)
from connectfour.views.gui.util import flash

TITLE_ROW = 0
FEEDBACK_ROW = 1
MATRIX_ROW = 2
CONTROL_ROW = 3
FRAME_COLSPAN = 3


class GameFrame(object):
    """Full-window frame for actually playing the game."""

    def __init__(self, view):
        """Create the frame, including all its widgets.

        Args:
            view (GUIView): The view that this frame is for.
        """
        self.view = view
        self.num_rows = view.model.get_num_rows()
        self.num_columns = view.model.get_num_columns()
        self.num_to_win = view.model.get_num_to_win()

        self.frame = tk.Frame(self.view.window)
        self.frame.grid()

        self.widgets = {}
        self._create_widgets()

    def remove(self):
        self.frame.grid_remove()

    ###################
    # Widget creation #
    ###################

    def _create_widgets(self):
        self._create_title()
        self._create_feedback_bar()
        self._create_game_matrix()
        self._create_controls()

    def _create_title(self):
        game_title = tk.Label(self.frame,
                              text=GAME_TEXT['title'].format(self.num_to_win))
        game_title.grid(row=TITLE_ROW, columnspan=FRAME_COLSPAN)

    def _create_feedback_bar(self):
        game_feedback = tk.Label(self.frame)
        game_feedback.grid(row=FEEDBACK_ROW, columnspan=FRAME_COLSPAN)
        self.widgets['game_feedback'] = game_feedback

    def _create_game_matrix(self):
        matrix_frame = tk.Frame(self.frame)
        matrix_frame.grid(row=MATRIX_ROW, columnspan=FRAME_COLSPAN)
        self.widgets['matrix_frame'] = matrix_frame

        self._create_play_buttons()
        self._create_squares()

    def _create_play_buttons(self):
        # 1D array of pointers to the disc-playing buttons (one per column)
        play_buttons = []

        for column in range(self.num_columns):
            button = tk.Button(
                self.widgets['matrix_frame'], text=GAME_TEXT['play'],
                command=lambda i=column: self.view.play_disc(i))
            button.grid(row=0, column=column)

            play_buttons.append(button)

        self.widgets['play_buttons'] = play_buttons

    def _create_squares(self):
        # 2D array of pointers to the square widgets making up game board
        squares = [[None for column in range(self.num_columns)]
                   for row in range(self.num_rows)]

        for row in range(self.num_rows):
            for column in range(self.num_columns):
                square = tk.Frame(self.widgets['matrix_frame'],
                                  width=SQUARE_SIZE, height=SQUARE_SIZE,
                                  bg=SQUARE_BACKGROUND, bd=SQUARE_BORDER_WIDTH,
                                  relief=tk.RAISED)

                # Add one to account for play buttons
                square.grid(row=row+1, column=column)
                squares[row][column] = square

        self.widgets['squares'] = squares

    def _create_controls(self):
        quit_button = tk.Button(self.frame, text=GAME_TEXT['quit'],
                                command=self.view.quit)
        quit_button.grid(row=CONTROL_ROW, column=0)

        play_again_button = tk.Button(
            self.frame, text=GAME_TEXT['play_again'],
            command=self.view.play_again)
        play_again_button.grid(row=CONTROL_ROW, column=FRAME_COLSPAN-1)
        self.widgets['play_again_button'] = play_again_button

    ######################
    # Widget interaction #
    ######################

    def enable_play_buttons(self):
        """Enable the buttons to play discs in specific columns."""
        for button in self.widgets['play_buttons']:
            button.configure(state=tk.NORMAL)

    def disable_play_buttons(self):
        """Disable the buttons to play discs in specific columns."""
        for button in self.widgets['play_buttons']:
            button.configure(state=tk.DISABLED)

    def enable_play_again_button(self):
        """Enable the button to play another round."""
        self.widgets['play_again_button'].configure(state=tk.NORMAL)

    def disable_play_again_button(self):
        """Disable the button to play another round."""
        self.widgets['play_again_button'].configure(state=tk.DISABLED)

    def announce_next_player(self, player):
        """Update feedback bar to announce the next player.

        Args:
            player (ConnectFourPlayer): The player who should play next.
        """
        self._update_game_feedback(GAME_TEXT['next_player'].format(player))

    def announce_try_again(self, player, reason):
        """Update feedback bar to announce that a player should try again.

        Args:
            player (ConnectFourPlayer): The player who needs to try again.
            reason (TryAgainReason): The reason player needs to try again.
        """
        reason = REASON_TO_STR[reason]
        self._update_game_feedback(GAME_TEXT['try_again']
                                   .format(player, reason))

    def announce_win(self, player):
        """Update feedback bar to announce that the round was won.

        Args:
            player (ConnectFourPlayer): The winner.
        """
        self._update_game_feedback(GAME_TEXT['win'].format(player))

    def announce_draw(self):
        """Update feedback bar to announce the the round ended in a draw."""

        self._update_game_feedback(GAME_TEXT['draw'])

    def _update_game_feedback(self, text):
        self.widgets['game_feedback'].configure(text=text)

    def update_square(self, player, position):
        """Paint a game square to reflect a disc played in that position.

        Args:
            player (ConnectFourPlayer): The player who played a disc here.
                Used to determine what color to paint the square.
            position: A 2-tuple in format (row, column).
        """
        row, column = position
        color = COLOR_TO_TK[player.get_color()]
        self.widgets['squares'][row][column].configure(bg=color)

    def flash_squares(self, positions):
        """Flash some of the game squares.

        Args:
            positions (set): A set of 2-tuples in format (row, column)
                of the positions to flash.
        """
        for row, column in positions:
            flash(element=self.widgets['squares'][row][column],
                  window=self.view.window, color=SQUARE_BACKGROUND)

    def reset_squares(self):
        """Recreate the game matrix to start a new round."""
        # self.widgets['matrix_frame'].grid_forget()
        '''
        Calling .destroy() or .grid_forget() here, or even at the
        end of _create_game_matrix(), causes the GUI screen to jump,
        since the old matrix is removed faster than the new is drawn.

        For now, I'm just letting the matrices pile up.

        Possible solution:
        Keep track of previous two games. Destroy 2-ago game.
        '''
        self._create_game_matrix()
