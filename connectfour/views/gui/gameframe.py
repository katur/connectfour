import Tkinter as tk

from util import flash
from config import (
    COLOR_TO_TK, REASON_TO_STR, GAME_TITLE_TEXT, PLAY_AGAIN_TEXT, QUIT_TEXT,
    COLUMN_TEXT, SQUARE_BACKGROUND, SQUARE_SIZE, SQUARE_BORDER_WIDTH,
)


class GameFrame(object):
    """Screen for actually playing game."""

    def __init__(self, view):
        self.view = view
        self.num_rows = view.model.get_num_rows()
        self.num_columns = view.model.get_num_columns()

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
        TITLE_ROW = 0
        FEEDBACK_ROW = 1
        COLUMN_BUTTONS_ROW = 2
        GRID_ROW = 3
        CONTROL_ROW = 4

        self._create_game_title_row(TITLE_ROW)
        self._create_game_feedback_row(FEEDBACK_ROW)
        self._create_column_buttons_row(COLUMN_BUTTONS_ROW)
        self._create_game_squares(GRID_ROW)
        self._create_game_control_row(CONTROL_ROW)

    def _create_game_title_row(self, row):
        game_title = tk.Label(self.frame, text=GAME_TITLE_TEXT)
        game_title.grid(row=row)

    def _create_game_feedback_row(self, row):
        game_feedback = tk.Label(self.frame)
        game_feedback.grid(row=row)
        self.widgets['game_feedback'] = game_feedback

    def _create_column_buttons_row(self, row):
        column_buttons_frame = tk.Frame(self.frame)
        column_buttons_frame.grid(row=row)

        column_buttons = []
        for column in range(self.num_columns):
            button = tk.Button(
                column_buttons_frame, text=COLUMN_TEXT,
                command=lambda i=column: self.view.play_disc(i))
            button.grid(row=0, column=column)
            column_buttons.append(button)

        self.widgets['column_buttons'] = column_buttons

    def _create_game_squares(self, outer_row):
        squares_frame = tk.Frame(self.frame)
        squares_frame.grid(row=outer_row)

        # Create 2D array to hold pointers to slot widgets
        squares = [[None for column in range(self.num_columns)]
                   for row in range(self.num_rows)]

        for row in range(self.num_rows):
            for column in range(self.num_columns):
                square = tk.Frame(squares_frame,
                                  width=SQUARE_SIZE, height=SQUARE_SIZE,
                                  bg=SQUARE_BACKGROUND, bd=SQUARE_BORDER_WIDTH,
                                  relief=tk.RAISED)
                square.grid(row=row, column=column)
                squares[row][column] = square

        self.widgets['squares_frame'] = squares_frame
        self.widgets['squares'] = squares

    def _create_game_control_row(self, row):
        control_frame = tk.Frame(self.frame)
        control_frame.grid(row=row)

        play_again_button = tk.Button(control_frame, text=PLAY_AGAIN_TEXT,
                                      command=self.view.play_again)
        play_again_button.grid(row=row, column=0)
        self.widgets['play_again_button'] = play_again_button

        game_quit_button = tk.Button(control_frame, text=QUIT_TEXT,
                                     command=self.view.quit)
        game_quit_button.grid(row=row, column=1)

    ######################
    # Widget interaction #
    ######################

    def enable_column_buttons(self):
        for button in self.widgets['column_buttons']:
            button.configure(state=tk.NORMAL)

    def disable_column_buttons(self):
        for button in self.widgets['column_buttons']:
            button.configure(state=tk.DISABLED)

    def enable_play_again_button(self):
        self.widgets['play_again_button'].configure(state=tk.NORMAL)

    def disable_play_again_button(self):
        self.widgets['play_again_button'].configure(state=tk.DISABLED)

    def update_square(self, player, position):
        row, column = position
        color = COLOR_TO_TK[player.get_color()]
        self.widgets['squares'][row][column].configure(bg=color)

    def update_game_feedback(self, text):
        self.widgets['game_feedback'].configure(text=text)

    def announce_next_player(self, player):
        self.update_game_feedback("{}'s turn".format(player))

    def announce_try_again(self, player, reason):
        reason = REASON_TO_STR[reason]
        self.update_game_feedback('{} try again ({})'.format(player, reason))

    def announce_winner(self, player):
        self.update_game_feedback('{} won the round'.format(player))

    def announce_draw(self):
        self.update_game_feedback('Round ended in a draw')

    def flash_squares(self, winning_positions):
        for row, column in winning_positions:
            flash(element=self.widgets['squares'][row][column],
                  window=self.view.window, color=SQUARE_BACKGROUND)
