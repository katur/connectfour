import Tkinter as tk

from connectfour.model.color import Color, get_color_list


PADDING = 20
SETUP_TITLE = (
    'Welcome to Connect Four! '
    'Please select game parameters and add players.'
)
GAME_TITLE = (
    'Welcome to Connect Four!'
)


def color_to_tk(color):
    colors = {
        Color.black: 'Black',
        Color.red: 'Red',
        Color.blue: 'Blue',
        Color.purple: 'Purple',
        Color.orange: 'Orange',
        Color.green: 'Green',
        Color.pink: 'Pink',
        Color.dark_green: 'DarkGreen',
        Color.brown: 'Brown',
        Color.gray: 'Gray',
    }
    return colors[color]


def enable_button(button):
    button.configure(state=tk.NORMAL)


def disable_button(button):
    button.configure(state=tk.DISABLED)


class GUIView(object):

    def __init__(self, game):
        self.game = game
        game.add_listener(self)

        self.num_rows = game.get_num_rows()
        self.num_columns = game.get_num_columns()
        self.colors = get_color_list()

        window = tk.Tk()
        window.title('Connect Four')
        self.main_frame = tk.Frame(window)
        self.main_frame.grid()
        self.create_setup_frame()
        window.mainloop()

        try:
            window.destroy()
        except Exception:
            pass

    #######################
    # Setup Frame Widgets #
    #######################

    def create_setup_frame(self):
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
        self.add_player_entry = tk.Entry(self.setup_frame)
        self.add_player_entry.grid(row=row, column=0, pady=PADDING)

        add_player_button = tk.Button(self.setup_frame, text='Add Player',
                                      command=self.add_player)
        add_player_button.grid(row=row, column=1)

    def _create_player_feedback_row(self, row):
        self.player_feedback = tk.Message(self.setup_frame, width=500)
        self.player_feedback.grid(row=row, columnspan=2)

    def _create_setup_control_row(self, row):
        self.start_game_button = tk.Button(self.setup_frame, text='Start Game',
                                           command=self.start_game,
                                           pady=PADDING)
        self.start_game_button.grid(row=row, column=0)
        disable_button(self.start_game_button)

        setup_quit = tk.Button(self.setup_frame, text='Quit',
                               command=self.main_frame.quit)
        setup_quit.grid(row=row, column=1)

    ######################
    # Game Frame Widgets #
    ######################

    def create_game_frame(self):
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
        self._create_grid(GRID_START_ROW)
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
                               command=lambda i=column: self.play_disc(i))
            button.grid(row=row, column=column)
            self.column_buttons.append(button)

    def _create_grid(self, start_row):
        SLOT_SIZE = 50
        SLOT_BORDER_WIDTH = 5
        SLOT_COLOR = 'Yellow'

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
        self.play_again_button = tk.Button(self.game_frame, text='Play Again',
                                           command=self.play_again)
        self.play_again_button.grid(row=row, column=0, columnspan=2)

        quit = tk.Button(self.game_frame, text='Quit',
                         command=self.main_frame.quit)
        quit.grid(row=row, column=2, columnspan=2)

    #################################
    # Button (de)activation helpers #
    #################################

    def enable_column_buttons(self):
        for button in self.column_buttons:
            enable_button(button)

    def disable_column_buttons(self):
        for button in self.column_buttons:
            disable_button(button)

    ######################
    # Callbacks to model #
    ######################

    def add_player(self):
        name = self.add_player_entry.get()
        color = self.colors[0]
        del self.colors[0]
        self.game.add_player(name, color)

    def start_game(self):
        self.setup_frame.grid_forget()
        self.create_game_frame()
        self.game.start_round()

    def play_again(self):
        self.game_frame.grid_forget()
        self.create_game_frame()
        self.game.start_round()

    def play_disc(self, column):
        self.game.play_disc(column)

    ################################
    # Respond to events from model #
    ################################

    def player_added(self, player):
        self.player_feedback.configure(text=(
            'Welcome, {}\n'
            'Total players added: {}'
            .format(player, self.game.get_num_players())))

        # Only one player is needed to enable start button
        enable_button(self.start_game_button)

    def round_started(self, round_number):
        disable_button(self.play_again_button)
        self.enable_column_buttons()

    def next_player(self, player):
        self.game_feedback.configure(text="{}'s turn".format(player))

    def try_again(self, player, reason):
        self.game_feedback.configure(text='{} try again ({})'
                                     .format(player, reason))

    def disc_played(self, player, position):
        row, column = position
        self.slots[row][column].configure(
            background=color_to_tk(player.disc.color))

    def round_won(self, player, winning_positions):
        self.game_feedback.configure(text='{} won the round'.format(player))
        self.disable_column_buttons()
        enable_button(self.play_again_button)

    def round_draw(self):
        self.game_feedback.configure(text='Round ended in a draw')
        self.disable_column_buttons()
        enable_button(self.play_again_button)
