import Tkinter as tk

from connectfour.config import DEFAULT_ROWS, DEFAULT_COLUMNS, DEFAULT_TO_WIN
from config import (
    PAD, SETUP_TITLE_TEXT, ADD_PLAYER_TEXT, PLAYER_FEEDBACK_TEXT,
    LAUNCH_GAME_TEXT, QUIT_TEXT,
)

TITLE_ROW = 0
DIMENSIONS_ROW = 1
ADD_PLAYER_ROW = 2
PLAYER_FEEDBACK_ROW = 3
CONTROL_ROW = 4


class SetupFrame(object):
    """Initial screen, for setting up game."""

    def __init__(self, view):
        self.view = view
        self.frame = tk.Frame(view.window)
        self.frame.grid(padx=PAD, pady=PAD)

        self.widgets = {}
        self._create_widgets()

    def remove(self):
        self.frame.grid_remove()

    ###################
    # Widget creation #
    ###################

    def _create_widgets(self):
        self._create_setup_title_row()
        self._create_dimensions_row()
        self._create_add_player_row()
        self._create_player_feedback_row()
        self._create_setup_control_row()

    def _create_setup_title_row(self):
        setup_title = tk.Label(self.frame, text=SETUP_TITLE_TEXT)
        setup_title.grid(row=TITLE_ROW, columnspan=3)

    def _create_dimensions_row(self):
        self._create_dimension_pair(
            position=(DIMENSIONS_ROW, 0), text='Rows:',
            default=str(DEFAULT_ROWS), widget_name='row_entry')

        self._create_dimension_pair(
            position=(DIMENSIONS_ROW, 1), text='Columns:',
            default=str(DEFAULT_COLUMNS), widget_name='column_entry')

        self._create_dimension_pair(
            position=(DIMENSIONS_ROW, 2), text='To Win:',
            default=str(DEFAULT_TO_WIN), widget_name='to_win_entry')

    def _create_dimension_pair(self, position, text, default, widget_name):
        row, column = position

        frame = tk.Frame(self.frame)
        frame.grid(row=row, column=column, padx=PAD, pady=PAD)

        prompt = tk.Label(frame, text=text)
        prompt.grid(row=0, column=0)

        entry = tk.Entry(frame, width=2)
        entry.insert(tk.END, default)
        entry.grid(row=0, column=1)
        self.widgets[widget_name] = entry

    def _create_add_player_row(self):
        player_entry = tk.Entry(self.frame)
        player_entry.grid(row=ADD_PLAYER_ROW, column=0, columnspan=2, pady=PAD)
        self.widgets['player_entry'] = player_entry

        add_player_button = tk.Button(self.frame,
                                      text=ADD_PLAYER_TEXT,
                                      command=self.view.add_player)
        add_player_button.grid(row=ADD_PLAYER_ROW, column=2)
        self.widgets['add_player_button'] = add_player_button

    def _create_player_feedback_row(self):
        player_feedback = tk.Message(self.frame, width=500)
        player_feedback.grid(row=PLAYER_FEEDBACK_ROW, columnspan=3, pady=PAD)
        self.widgets['player_feedback'] = player_feedback

    def _create_setup_control_row(self):
        setup_quit_button = tk.Button(self.frame, text=QUIT_TEXT,
                                      command=self.view.quit)
        setup_quit_button.grid(row=CONTROL_ROW, column=0)

        launch_button = tk.Button(self.frame, text=LAUNCH_GAME_TEXT,
                                  state=tk.DISABLED,
                                  command=self.view.launch_game)
        launch_button.grid(row=CONTROL_ROW, column=2)
        self.widgets['launch_button'] = launch_button

    ######################
    # Widget interaction #
    ######################

    def parse_player_entry(self):
        name = self.widgets['player_entry'].get()
        self.widgets['player_entry'].delete(0, tk.END)
        return name

    def parse_row_entry(self):
        return int(self.widgets['row_entry'].get())

    def parse_column_entry(self):
        return int(self.widgets['column_entry'].get())

    def parse_to_win_entry(self):
        return int(self.widgets['to_win_entry'].get())

    def update_player_feedback(self, player, num_players):
        self.widgets['player_feedback'].configure(
            text=PLAYER_FEEDBACK_TEXT.format(player, num_players))

    def enable_launch_button(self):
        self.widgets['launch_button'].configure(state=tk.NORMAL)
