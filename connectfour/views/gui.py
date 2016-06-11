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
        Color.yellow: 'Yellow',
        Color.blue: 'Blue',
        Color.orange: 'Orange',
        Color.green: 'Green',
        Color.purple: 'Purple',
        Color.pink: 'Pink',
        Color.light_green: 'LightGreen',
        Color.brown: 'Brown',
    }
    return colors[color]


class GUIView(object):

    def __init__(self, game):
        self.game = game
        game.add_listener(self)

        self.num_rows = game.get_num_rows()
        self.num_columns = game.get_num_columns()
        self.colors = get_color_list()

        window = tk.Tk()
        window.title('Connect Four')
        self.frame = tk.Frame(window)
        self.frame.grid()
        self.create_setup_frame()
        window.mainloop()

        try:
            window.destroy()
        except Exception:
            pass

    #######################
    # GUI Widget Creation #
    #######################

    def create_setup_frame(self):
        self.setup_frame = tk.Frame(self.frame, padx=PADDING, pady=PADDING)
        self.setup_frame.grid()

        setup_title = tk.Message(self.setup_frame, text=SETUP_TITLE, width=500,
                                 pady=PADDING)
        setup_title.grid(row=0, columnspan=2)

        self.player_entry = tk.Entry(self.setup_frame)
        self.player_entry.grid(row=1, column=0, pady=PADDING)

        player_button = tk.Button(self.setup_frame, text='Add player',
                                  command=self.add_player)
        player_button.grid(row=1, column=1)

        self.player_count = tk.Label(self.setup_frame)
        self.player_count.grid(row=2, columnspan=2)

        start_button = tk.Button(self.setup_frame, text='Start game',
                                 command=self.start_game,
                                 pady=PADDING)
        start_button.grid(row=3, column=0)

        quit = tk.Button(self.setup_frame, text='Quit',
                         command=self.frame.quit)
        quit.grid(row=3, column=1)

    def create_game_frame(self):
        self.game_frame = tk.Frame(self.frame)
        self.game_frame.grid()

        game_title = tk.Message(self.game_frame, text=GAME_TITLE, width=500)
        game_title.grid(row=0, columnspan=self.num_columns)

        self.feedback = tk.Label(self.game_frame)
        self.feedback.grid(row=1, columnspan=self.num_columns)

        self.column_buttons = []
        for column in range(self.num_columns):
            button = tk.Button(self.game_frame, text='Play',
                               command=lambda i=column: self.play_disc(i))
            button.grid(row=2, column=column)
            self.column_buttons.append(button)

        # Create 2D array to hold pointers to position widgets
        self.slots = [[None for column in range(self.num_columns)]
                      for row in range(self.num_rows)]

        start_row = 4
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                slot = tk.Frame(self.game_frame,
                                width=50, height=50,
                                background='Yellow',
                                borderwidth=5, relief=tk.RAISED)
                slot.grid(row=row + start_row, column=column)
                self.slots[row][column] = slot

        play_again = tk.Button(self.game_frame, text='Play Again',
                               command=self.new_round)
        play_again.grid(row=start_row + self.num_rows + 1, columnspan=2)

    ######################
    # Callbacks to model #
    ######################

    def add_player(self):
        name = self.player_entry.get()
        color = self.colors[0]
        del self.colors[0]

        self.game.add_player(name, color)

    def start_game(self):
        self.setup_frame.grid_forget()
        self.create_game_frame()
        self.game.start_round()

    def new_round(self):
        self.game_frame.grid_forget()
        self.create_game_frame()
        self.game.start_round()

    def play_disc(self, column):
        self.game.play_disc(column)

    ################################
    # Respond to events from model #
    ################################

    def player_added(self, player):
        self.player_count.configure(text='Welcome, {}'.format(player))
        self.player_entry.delete(0, tk.END)

    def round_started(self, round_number):
        pass

    def next_player(self, player):
        self.feedback.configure(text="{}'s turn".format(player))

    def try_again(self, player, reason):
        pass

    def disc_played(self, player, position):
        row, column = position
        self.slots[row][column].configure(
            background=color_to_tk(player.disc.color))

    def round_won(self, player, winning_positions):
        pass

    def round_draw(self):
        pass
