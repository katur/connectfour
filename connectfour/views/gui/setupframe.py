import Tkinter as tk

from connectfour.config import DEFAULT_ROWS, DEFAULT_COLUMNS, DEFAULT_TO_WIN
from connectfour.views.gui.config import PAD, SETUP_TEXT

TITLE_ROW = 0
SETTINGS_ROW = 1
ADD_PLAYER_ROW = 2
FEEDBACK_ROW = 3
CONTROL_ROW = 4
FRAME_COLSPAN = 3


class SetupFrame(object):
    """Full-window frame for game setup."""

    def __init__(self, view):
        """Create the frame, including all its widgets.

        Args:
            view (GUIView): The view that this frame is for.
        """
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
        self._create_title()
        self._create_settings_admin()
        self._create_add_player_admin()
        self._create_feedback_area()
        self._create_controls()

    def _create_title(self):
        setup_title = tk.Label(self.frame, text=SETUP_TEXT['title'])
        setup_title.grid(row=TITLE_ROW, columnspan=FRAME_COLSPAN)

    def _create_settings_admin(self):
        self._create_labelled_entry(
            position=(SETTINGS_ROW, 0), text=SETUP_TEXT['rows'],
            default=str(DEFAULT_ROWS), widget_name='row_entry')

        self._create_labelled_entry(
            position=(SETTINGS_ROW, 1), text=SETUP_TEXT['columns'],
            default=str(DEFAULT_COLUMNS), widget_name='column_entry')

        self._create_labelled_entry(
            position=(SETTINGS_ROW, 2), text=SETUP_TEXT['to_win'],
            default=str(DEFAULT_TO_WIN), widget_name='to_win_entry')

    def _create_labelled_entry(self, position, text, default, widget_name):
        row, column = position

        frame = tk.Frame(self.frame)
        frame.grid(row=row, column=column, padx=PAD, pady=PAD)

        prompt = tk.Label(frame, text=text)
        prompt.grid(row=0, column=0)

        entry = tk.Entry(frame, width=2)
        entry.insert(tk.END, default)
        entry.grid(row=0, column=1)
        self.widgets[widget_name] = entry

    def _create_add_player_admin(self):
        player_entry = tk.Entry(self.frame)
        player_entry.grid(row=ADD_PLAYER_ROW, column=0,
                          columnspan=FRAME_COLSPAN-1, pady=PAD)
        self.widgets['player_entry'] = player_entry

        add_player_button = tk.Button(self.frame,
                                      text=SETUP_TEXT['add_player'],
                                      command=self.view.add_player)
        add_player_button.grid(row=ADD_PLAYER_ROW, column=FRAME_COLSPAN-1)
        self.widgets['add_player_button'] = add_player_button

    def _create_feedback_area(self):
        feedback = tk.Message(self.frame, width=500)
        feedback.grid(row=FEEDBACK_ROW, columnspan=FRAME_COLSPAN, pady=PAD)
        self.widgets['feedback'] = feedback

    def _create_controls(self):
        quit_button = tk.Button(self.frame, text=SETUP_TEXT['quit'],
                                command=self.view.quit)
        quit_button.grid(row=CONTROL_ROW, column=0)

        launch_button = tk.Button(self.frame, text=SETUP_TEXT['launch'],
                                  state=tk.DISABLED,
                                  command=self.view.launch_game)
        launch_button.grid(row=CONTROL_ROW, column=FRAME_COLSPAN-1)
        self.widgets['launch_button'] = launch_button

    ######################
    # Widget interaction #
    ######################

    def enable_launch_button(self):
        """Enable the button to start the game."""
        self.widgets['launch_button'].configure(state=tk.NORMAL)

    def parse_row_entry(self):
        """Get the contents of the row entry field.

        Returns:
            str: Text entered into the row field, or empty string if
                nothing entered.
        """
        # Do not cast to int here, to give caller more flexibility
        # in error checking or casting
        return self.widgets['row_entry'].get()

    def parse_column_entry(self):
        """Get the contents of the column entry field.

        Returns:
            str: Text entered into the column field, or empty string if
                nothing entered.
        """
        return self.widgets['column_entry'].get()

    def parse_to_win_entry(self):
        """Get the contents of the "to win" entry field.

        Returns:
            str: Text entered into the "to win" field, or empty string if
                nothing entered.
        """
        return self.widgets['to_win_entry'].get()

    def parse_player_entry(self):
        """Get the contents of the player entry field, and clear the field.

        Returns:
            str: Text entered into the player field, or empty string if
                nothing entered.
        """
        name = self.widgets['player_entry'].get()
        self.widgets['player_entry'].delete(0, tk.END)
        return name

    def update_feedback(self, player, num_players):
        """Update the feedback to reflect that a new player was added.

        Args:
            player (Player): A new player that was added to the game.
            num_players (int): The current player count.
        """
        self.widgets['feedback'].configure(
            text=SETUP_TEXT['feedback'].format(player, num_players))
