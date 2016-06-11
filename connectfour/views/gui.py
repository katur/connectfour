import Tkinter as tk

from connectfour import pubsub

from connectfour.util.color import get_color_list
from connectfour.views.gui_config import (
    WINDOW_TITLE, SETUP_TITLE, GAME_TITLE, PLAYER_FEEDBACK_TEXT,
    SLOT_COLOR, SLOT_SIZE, SLOT_BORDER_WIDTH,
    COLOR_TO_TK, PADDING,
)

COLORS = get_color_list()


class GUIView(object):

    def __init__(self, game):
        self.game = game
        self.num_rows = game.get_num_rows()
        self.num_columns = game.get_num_columns()

        self._create_subscriptions()

        # Initialize GUI wrappers
        window = tk.Tk()
        window.title(WINDOW_TITLE)
        self.main_frame = tk.Frame(window)
        self.main_frame.grid()

        # Initialize and launch setup screen
        self._create_setup_frame()
        window.mainloop()

        # Cleanup once main loop ends
        try:
            window.destroy()
        except Exception:
            # TODO: How to handle this?
            pass

    def _create_subscriptions(self):
        responses = {
            pubsub.Action.player_added: self._on_player_added,
            pubsub.Action.round_started: self._on_round_started,
            pubsub.Action.next_player: self._on_next_player,
            pubsub.Action.try_again: self._on_try_again,
            pubsub.Action.disc_played: self._on_disc_played,
            pubsub.Action.round_won: self._on_round_won,
            pubsub.Action.round_draw: self._on_round_draw,
        }
        for action, response in responses.iteritems():
            pubsub.subscribe(action, response)

    ###########################
    # Widgets for Setup Frame #
    ###########################

    def _create_setup_frame(self):
        self.setup_frame = tk.Frame(self.main_frame, padx=PADDING,
                                    pady=PADDING)
        self.setup_frame.grid()
        self._create_setup_widgets()

    def _create_setup_widgets(self):
        TITLE_ROW = 0
        ADD_PLAYER_ROW = 1
        PLAYER_FEEDBACK_ROW = 2
        CONTROL_ROW = 3

        self._create_setup_title_row(TITLE_ROW)
        self._create_add_player_row(ADD_PLAYER_ROW)
        self._create_player_feedback_row(PLAYER_FEEDBACK_ROW)
        self._create_setup_control_row(CONTROL_ROW)

    def _create_setup_title_row(self, row):
        setup_title = tk.Label(self.setup_frame, text=SETUP_TITLE,
                               pady=PADDING)
        setup_title.grid(row=row, columnspan=2)

    def _create_add_player_row(self, row):
        self.player_entry = tk.Entry(self.setup_frame)
        self.player_entry.grid(row=row, column=0, pady=PADDING)

        add_player_button = tk.Button(self.setup_frame, text='Add Player',
                                      command=self._add_player)

        add_player_button.grid(row=row, column=1)

    def _create_player_feedback_row(self, row):
        self.player_feedback = tk.Message(self.setup_frame, width=500)
        self.player_feedback.grid(row=row, columnspan=2)

    def _create_setup_control_row(self, row):
        self.launch_game_button = tk.Button(self.setup_frame,
                                            text='Launch Game',
                                            command=self._launch_game,
                                            pady=PADDING)
        self.launch_game_button.grid(row=row, column=0)
        self.launch_game_button.configure(state=tk.DISABLED)

        setup_quit = tk.Button(self.setup_frame, text='Quit',
                               command=self.main_frame.quit)
        setup_quit.grid(row=row, column=1)

    ##########################
    # Widgets for Game Frame #
    ##########################

    def _create_game_frame(self):
        self.game_frame = tk.Frame(self.main_frame)
        self.game_frame.grid()
        self._create_game_widgets()

    def _create_game_widgets(self):
        TITLE_ROW = 0
        FEEDBACK_ROW = 1
        COLUMN_BUTTONS_ROW = 2
        GRID_START_ROW = 3
        CONTROL_ROW = GRID_START_ROW + self.num_rows

        self._create_game_title_row(TITLE_ROW)
        self._create_game_feedback_row(FEEDBACK_ROW)
        self._create_column_buttons_row(COLUMN_BUTTONS_ROW)
        self._create_game_grid(GRID_START_ROW)
        self._create_game_control_row(CONTROL_ROW)

    def _create_game_title_row(self, row):
        game_title = tk.Label(self.game_frame, text=GAME_TITLE)
        game_title.grid(row=row, columnspan=self.num_columns)

    def _create_game_feedback_row(self, row):
        self.game_feedback = tk.Label(self.game_frame)
        self.game_feedback.grid(row=row, columnspan=self.num_columns)

    def _create_column_buttons_row(self, row):
        self.column_buttons = []
        for column in range(self.num_columns):
            button = tk.Button(self.game_frame, text='Play',
                               command=lambda i=column: self._play_disc(i))
            button.grid(row=row, column=column)
            self.column_buttons.append(button)

    def _create_game_grid(self, start_row):
        # Create 2D array to hold pointers to slot widgets
        self.slots = [[None for column in range(self.num_columns)]
                      for row in range(self.num_rows)]

        for row in range(self.num_rows):
            for column in range(self.num_columns):
                slot = tk.Frame(self.game_frame,
                                width=SLOT_SIZE, height=SLOT_SIZE,
                                background=SLOT_COLOR,
                                borderwidth=SLOT_BORDER_WIDTH,
                                relief=tk.RAISED)
                slot.grid(row=row + start_row, column=column)
                self.slots[row][column] = slot

    def _create_game_control_row(self, row):
        self.play_again_button = tk.Button(self.game_frame,
                                           text='Play Again',
                                           command=self._play_again)
        self.play_again_button.grid(row=row, column=0, columnspan=2)

        quit = tk.Button(self.game_frame, text='Quit',
                         command=self.main_frame.quit)
        quit.grid(row=row, column=2, columnspan=2)

    #################################
    # Button (de)activation helpers #
    #################################
    def _enable_column_buttons(self):
        for button in self.column_buttons:
            button.configure(state=tk.NORMAL)

    def _disable_column_buttons(self):
        for button in self.column_buttons:
            button.configure(state=tk.DISABLED)

    ###########################################
    # Button callbacks (which call the model) #
    ###########################################

    def _add_player(self):
        name = self.player_entry.get()
        index = self.game.get_num_players()
        color = COLORS[index]
        self.game.add_player(name, color)
        self.player_entry.delete(0, 'end')

    def _launch_game(self):
        self.setup_frame.grid_forget()
        self._create_game_frame()
        self.game.start_round()

    def _play_again(self):
        self.game_frame.grid_forget()
        self._create_game_frame()
        self.game.start_round()

    def _play_disc(self, column):
        self.game.play_disc(column)

    ################################
    # Respond to events from model #
    ################################

    def _on_player_added(self, player):
        self.player_feedback.configure(text=(
            PLAYER_FEEDBACK_TEXT
            .format(player, self.game.get_num_players())))

        # Only one player is needed to enable start button
        self.launch_game_button.configure(state=tk.NORMAL)

    def _on_round_started(self, round_number):
        self.play_again_button.configure(state=tk.DISABLED)
        self._enable_column_buttons()

    def _on_next_player(self, player):
        self.game_feedback.configure(text="{}'s turn".format(player))

    def _on_try_again(self, player, reason):
        self.game_feedback.configure(text='{} try again ({})'
                                     .format(player, reason.name))

    def _on_disc_played(self, player, position):
        row, column = position
        self.slots[row][column].configure(
            background=COLOR_TO_TK[player.disc.color])

    def _on_round_won(self, player, winning_positions):
        self.game_feedback.configure(text='{} won the round'.format(player))
        self._disable_column_buttons()
        self.play_again_button.configure(state=tk.NORMAL)

    def _on_round_draw(self):
        self.game_feedback.configure(text='Round ended in a draw')
        self._disable_column_buttons()
        self.play_again_button.configure(state=tk.NORMAL)
