import Tkinter as tk

from util import flash
from config import (COLOR_TO_TK, REASON_TO_STR, GAME_TEXT,
                    SQUARE_BACKGROUND, SQUARE_SIZE, SQUARE_BORDER_WIDTH)

TITLE_ROW = 0
FEEDBACK_ROW = 1
MATRIX_ROW = 2
CONTROL_ROW = 3


class GameFrame(object):
    """Screen for actually playing game."""

    def __init__(self, view, num_rows, num_columns):
        self.view = view
        self.num_rows = num_rows
        self.num_columns = num_columns

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
        game_title = tk.Label(self.frame, text=GAME_TEXT['title'])
        game_title.grid(row=TITLE_ROW)

    def _create_feedback_bar(self):
        game_feedback = tk.Label(self.frame)
        game_feedback.grid(row=FEEDBACK_ROW)
        self.widgets['game_feedback'] = game_feedback

    def _create_game_matrix(self):
        matrix_frame = tk.Frame(self.frame)
        matrix_frame.grid(row=MATRIX_ROW)
        self.widgets['matrix_frame'] = matrix_frame

        self._create_play_buttons(matrix_frame)
        self._create_squares(matrix_frame)

    def _create_play_buttons(self, parent):
        play_buttons = []
        for column in range(self.num_columns):
            button = tk.Button(
                parent, text=GAME_TEXT['play'],
                command=lambda i=column: self.view.play_disc(i))
            button.grid(row=0, column=column)

            play_buttons.append(button)

        self.widgets['play_buttons'] = play_buttons

    def _create_squares(self, parent):
        # Create 2D array to hold pointers to slot widgets
        squares = [[None for column in range(self.num_columns)]
                   for row in range(self.num_rows)]

        for row in range(self.num_rows):
            for column in range(self.num_columns):
                square = tk.Frame(parent,
                                  width=SQUARE_SIZE, height=SQUARE_SIZE,
                                  bg=SQUARE_BACKGROUND, bd=SQUARE_BORDER_WIDTH,
                                  relief=tk.RAISED)

                # Add one to account for play buttons
                square.grid(row=row + 1, column=column)
                squares[row][column] = square

        self.widgets['squares'] = squares

    def _create_controls(self):
        control_frame = tk.Frame(self.frame)
        control_frame.grid(row=CONTROL_ROW)

        quit_button = tk.Button(control_frame, text=GAME_TEXT['quit'],
                                command=self.view.quit)
        quit_button.grid(row=0, column=0)

        play_again_button = tk.Button(
            control_frame, text=GAME_TEXT['play_again'],
            command=self.view.play_again)
        play_again_button.grid(row=0, column=1)
        self.widgets['play_again_button'] = play_again_button

    ######################
    # Widget interaction #
    ######################

    def enable_play_buttons(self):
        for button in self.widgets['play_buttons']:
            button.configure(state=tk.NORMAL)

    def disable_play_buttons(self):
        for button in self.widgets['play_buttons']:
            button.configure(state=tk.DISABLED)

    def enable_play_again_button(self):
        self.widgets['play_again_button'].configure(state=tk.NORMAL)

    def disable_play_again_button(self):
        self.widgets['play_again_button'].configure(state=tk.DISABLED)

    def update_square(self, player, position):
        row, column = position
        color = COLOR_TO_TK[player.get_color()]
        self.widgets['squares'][row][column].configure(bg=color)

    def announce_next_player(self, player):
        self._update_game_feedback(GAME_TEXT['next_player'].format(player))

    def announce_try_again(self, player, reason):
        reason = REASON_TO_STR[reason]
        self._update_game_feedback(GAME_TEXT['try_again']
                                   .format(player, reason))

    def announce_win(self, player):
        self._update_game_feedback(GAME_TEXT['win'].format(player))

    def announce_draw(self):
        self._update_game_feedback(GAME_TEXT['draw'])

    def _update_game_feedback(self, text):
        self.widgets['game_feedback'].configure(text=text)

    def flash_squares(self, winning_positions):
        for row, column in winning_positions:
            flash(element=self.widgets['squares'][row][column],
                  window=self.view.window, color=SQUARE_BACKGROUND)

    def reset_squares(self):
        '''
        Calling .destroy() or .grid_forget() here, or even at the
        end of _create_game_matrix(), causes the GUI screen to jump,
        since the old matrix is removed faster than the new is drawn.

        For now, I'm just letting the matrices pile up.

        Possible solution:
        Keep track of previous two games. Destroy game 2-ago.
        '''
        # self.widgets['matrix_frame'].grid_forget()

        self._create_game_matrix()
