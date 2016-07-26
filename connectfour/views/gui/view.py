import Tkinter as tk
import tkMessageBox

from connectfour.model import (DEFAULT_ROWS, DEFAULT_COLUMNS, DEFAULT_TO_WIN,
                               Color)
from connectfour.pubsub import ModelAction, ViewAction
from connectfour.views.gui import config
from connectfour.views.gui.util import flash
from connectfour.views.util import (get_stripped_nonempty_string,
                                    get_positive_int)


class GUIView(object):
    """View to play Connect Four in a Tkinter GUI."""

    def __init__(self, pubsub, model):
        """Create this view, which creates a Tkinter GUI in a new window.

        Args:
            model (ConnectFourModel): The model this view interacts with.
        """
        self.pubsub = pubsub
        self.model = model
        self._create_subscriptions()

        # Initialize GUI window
        self.window = tk.Tk()
        self.window.title(config.WINDOW_TITLE)

        # Initialize setup screen
        self.setup_frame = SetupFrame(self)

        # Start program
        self.window.mainloop()

    def _create_subscriptions(self):
        responses = {
            ModelAction.player_added: self.on_player_added,
            ModelAction.game_started: self.on_game_started,
            ModelAction.next_player: self.on_next_player,
            ModelAction.try_again: self.on_try_again,
            ModelAction.color_played: self.on_color_played,
            ModelAction.game_won: self.on_game_won,
            ModelAction.game_draw: self.on_game_draw,
        }

        for action, response in responses.iteritems():
            self.pubsub.subscribe(action, response)

    def quit(self):
        """Quit the game."""
        self.window.quit()

    ###########################
    # Respond to model events #
    ###########################

    def on_player_added(self, player):
        """Respond to the model reporting that a player was added to the game.

        Args:
            player (Player): The player that was added.
        """
        self.setup_frame.update_feedback(player, self.model.get_num_players())

        # Enable launch once first player is added
        self.setup_frame.enable_launch_button()

    def on_game_started(self, game_number):
        """Respond to the model reporting that a new game started.

        Args:
            game_number (int): The number of the game that started.
        """
        self.game_frame.disable_play_again_button()
        self.game_frame.enable_play_buttons()

    def on_next_player(self, player):
        """Respond to the model reporting the next player.

        Args:
            player (Player): The player who should play next.
        """
        self.game_frame.announce_next_player(player)

        if player.is_ai:
            self.game_frame.disable_play_buttons()
            self.pubsub.publish(ViewAction.request_ai_play)
        else:
            self.game_frame.enable_play_buttons()

        self.pubsub.do_queue()

    def on_try_again(self, player, reason):
        """Respond to the model reporting a try again event.

        Args:
            player (Player): The player who should try again.
            reason (TryAgainReason): The reason the player should try again.
        """
        self.game_frame.announce_try_again(player, reason)

    def on_color_played(self, color, position):
        """Respond to the model reporting that a color was played.

        Args:
            color (Color): The color that was played.
            position: A 2-tuple in format (row, column) of the position the
                color was played.
        """
        self.game_frame.update_square(color, position)

    def on_game_won(self, player, winning_positions):
        """Respond to the model reporting that a game was won.

        Args:
            player (Player): The winner.
            winning_positions: The positions that resulted in the win.
        """
        self.game_frame.announce_win(player)
        self.game_frame.disable_play_buttons()
        self.game_frame.enable_play_again_button()
        self.game_frame.flash_squares(winning_positions)

    def on_game_draw(self):
        """Respond to the model reporting that a game ended in a draw."""
        self.game_frame.announce_draw()
        self.game_frame.disable_play_buttons()
        self.game_frame.enable_play_again_button()

    ##################
    # Call the model #
    ##################

    def add_player(self):
        """Tell the model to add a player.

        This method parses player attributes from user input. If input is
        invalid, a popup appears alerting the user to fix the error.
        """
        try:
            name = get_stripped_nonempty_string(
                self.setup_frame.parse_player_entry(),
                name='Name', max_len=config.MAX_NAME_LENGTH)
            is_ai = self.setup_frame.parse_is_ai_bool()
        except ValueError as e:
            tkMessageBox.showerror(config.ALERT_TEXT['title'], e)
            return

        color = Color(self.model.get_num_players())
        self.pubsub.publish(ViewAction.add_player, name, color, is_ai)
        self.pubsub.do_queue()

    def launch_game_frame(self):
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
            tkMessageBox.showerror(config.ALERT_TEXT['title'], e)
            return

        # Move on to game frame
        self.setup_frame.remove()
        self.game_frame = GameFrame(self)
        self.pubsub.publish(ViewAction.start_game)
        self.pubsub.do_queue()

    def _create_board(self):
        num_rows = get_positive_int(
            self.setup_frame.parse_row_entry(),
            name='Rows', max_value=config.MAX_ROWS)
        num_columns = get_positive_int(
            self.setup_frame.parse_column_entry(),
            name='Columns', max_value=config.MAX_COLUMNS)
        num_to_win = get_positive_int(
            self.setup_frame.parse_to_win_entry(),
            name='To Win', max_value=config.MAX_TO_WIN)

        self.pubsub.publish(
            ViewAction.create_board, num_rows, num_columns, num_to_win)
        self.pubsub.do_queue()

    def start_new_game(self):
        """Tell the model to start a new game.

        This method also clears the game squares for the new game.
        """
        self.game_frame.reset_squares()
        self.pubsub.publish(ViewAction.start_game)
        self.pubsub.do_queue()

    def play(self, column):
        """Tell the model to make a play in a column.

        The play is assumed to be by the current player.

        Args:
            column (int): The column to play in.
        """
        self.pubsub.publish(ViewAction.play, column)
        self.pubsub.do_queue()


class SetupFrame(object):
    """Full-window frame for game setup."""

    def __init__(self, view):
        """Create the frame, including all its widgets.

        Args:
            view (GUIView): The view that this frame is for.
        """
        self.view = view
        self.frame = tk.Frame(view.window)
        self.frame.grid(padx=config.PAD, pady=config.PAD)

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
        setup_title = tk.Label(self.frame, text=config.SETUP_TEXT['title'])
        setup_title.grid(row=config.SETUP_ROWS['title'],
                         columnspan=config.SETUP_COLSPAN)

    def _create_settings_admin(self):
        row = config.SETUP_ROWS['settings']
        self._create_labelled_entry(
            position=(row, 0), text=config.SETUP_TEXT['rows'],
            default=str(DEFAULT_ROWS), widget_name='row_entry')

        self._create_labelled_entry(
            position=(row, 1), text=config.SETUP_TEXT['columns'],
            default=str(DEFAULT_COLUMNS), widget_name='column_entry')

        self._create_labelled_entry(
            position=(row, 2), text=config.SETUP_TEXT['to_win'],
            default=str(DEFAULT_TO_WIN), widget_name='to_win_entry')

    def _create_labelled_entry(self, position, text, default, widget_name):
        row, column = position

        frame = tk.Frame(self.frame)
        frame.grid(row=row, column=column, padx=config.PAD, pady=config.PAD)

        prompt = tk.Label(frame, text=text)
        prompt.grid(row=0, column=0)

        entry = tk.Entry(frame, width=2)
        entry.insert(tk.END, default)
        entry.grid(row=0, column=1)
        self.widgets[widget_name] = entry

    def _create_add_player_admin(self):
        row = config.SETUP_ROWS['add_player']

        player_entry = tk.Entry(self.frame)
        player_entry.grid(row=row, column=0, columnspan=config.SETUP_COLSPAN-2,
                          pady=config.PAD)
        self.widgets['player_entry'] = player_entry

        is_ai_bool = tk.BooleanVar()
        self.widgets['is_ai_bool'] = is_ai_bool

        player_radio = tk.Frame(self.frame)
        player_radio.grid(row=row, column=1)

        human_button = tk.Radiobutton(player_radio, text='Human',
                                      variable=is_ai_bool, value=False)
        ai_button = tk.Radiobutton(player_radio, text='AI',
                                   variable=is_ai_bool, value=True)
        human_button.grid(row=0, column=0)
        ai_button.grid(row=1, column=0)

        add_player_button = tk.Button(self.frame, command=self.view.add_player,
                                      text=config.SETUP_TEXT['add_player'])
        add_player_button.grid(row=row, column=config.SETUP_COLSPAN-1)
        self.widgets['add_player_button'] = add_player_button

    def _create_feedback_area(self):
        feedback = tk.Message(self.frame, width=500)
        feedback.grid(row=config.SETUP_ROWS['feedback'],
                      columnspan=config.SETUP_COLSPAN, pady=config.PAD)
        self.widgets['feedback'] = feedback

    def _create_controls(self):
        row = config.SETUP_ROWS['control']

        quit_button = tk.Button(self.frame, command=self.view.quit,
                                text=config.SETUP_TEXT['quit'])
        quit_button.grid(row=row, column=0)

        launch_button = tk.Button(self.frame,
                                  command=self.view.launch_game_frame,
                                  text=config.SETUP_TEXT['launch'],
                                  state=tk.DISABLED)
        launch_button.grid(row=row, column=config.SETUP_COLSPAN-1)
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

    def parse_is_ai_bool(self):
        """Get the contents of the is_ai_bool variable.

        Returns:
            int:
        """
        return self.widgets['is_ai_bool'].get()

    def update_feedback(self, player, num_players):
        """Update the feedback to reflect that a new player was added.

        Args:
            player (Player): The player that was added to the game.
            num_players (int): The current player count.
        """
        self.widgets['feedback'].configure(
            text=config.SETUP_TEXT['feedback'].format(player, num_players))


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
        game_title = tk.Label(
            self.frame,
            text=config.GAME_TEXT['title'].format(self.num_to_win))
        game_title.grid(row=config.GAME_ROWS['title'],
                        columnspan=config.GAME_COLSPAN)

    def _create_feedback_bar(self):
        game_feedback = tk.Label(self.frame)
        game_feedback.grid(row=config.GAME_ROWS['feedback'],
                           columnspan=config.GAME_COLSPAN)
        self.widgets['game_feedback'] = game_feedback

    def _create_game_matrix(self):
        matrix_frame = tk.Frame(self.frame)
        matrix_frame.grid(row=config.GAME_ROWS['matrix'],
                          columnspan=config.GAME_COLSPAN)
        self.widgets['matrix_frame'] = matrix_frame

        self._create_play_buttons()
        self._create_squares()

    def _create_play_buttons(self):
        # 1D array of pointers to the play buttons (one per column)
        play_buttons = []

        for column in range(self.num_columns):
            button = tk.Button(
                self.widgets['matrix_frame'], text=config.GAME_TEXT['play'],
                command=lambda i=column: self.view.play(i))
            button.grid(row=0, column=column)

            play_buttons.append(button)

        self.widgets['play_buttons'] = play_buttons

    def _create_squares(self):
        # 2D array of pointers to the square widgets making up game board
        squares = [[None for column in range(self.num_columns)]
                   for row in range(self.num_rows)]

        for row in range(self.num_rows):
            for column in range(self.num_columns):
                square = tk.Frame(
                    self.widgets['matrix_frame'], relief=tk.RAISED,
                    width=config.SQUARE_SIZE, height=config.SQUARE_SIZE,
                    bg=config.SQUARE_BACKGROUND, bd=config.SQUARE_BORDER_WIDTH)

                # Add one to account for play buttons
                square.grid(row=row+1, column=column)
                squares[row][column] = square

        self.widgets['squares'] = squares

    def _create_controls(self):
        row = config.GAME_ROWS['control']
        quit_button = tk.Button(self.frame, text=config.GAME_TEXT['quit'],
                                command=self.view.quit)
        quit_button.grid(row=row, column=0)

        play_again_button = tk.Button(
            self.frame, text=config.GAME_TEXT['play_again'],
            command=self.view.start_new_game)
        play_again_button.grid(row=row, column=config.GAME_COLSPAN-1)
        self.widgets['play_again_button'] = play_again_button

    ######################
    # Widget interaction #
    ######################

    def enable_play_buttons(self):
        """Enable the buttons to play in specific columns."""
        for button in self.widgets['play_buttons']:
            button.configure(state=tk.NORMAL)

    def disable_play_buttons(self):
        """Disable the buttons to play in specific columns."""
        for button in self.widgets['play_buttons']:
            button.configure(state=tk.DISABLED)

    def enable_play_again_button(self):
        """Enable the button to play another game."""
        self.widgets['play_again_button'].configure(state=tk.NORMAL)

    def disable_play_again_button(self):
        """Disable the button to play another game."""
        self.widgets['play_again_button'].configure(state=tk.DISABLED)

    def announce_next_player(self, player):
        """Update feedback bar to announce the next player.

        Args:
            player (Player): The player who should play next.
        """
        self._update_game_feedback(
            config.GAME_TEXT['next_player'].format(player))

    def announce_try_again(self, player, reason):
        """Update feedback bar to announce that a player should try again.

        Args:
            player (Player): The player who needs to try again.
            reason (TryAgainReason): The reason player needs to try again.
        """
        reason = config.REASON_TEXT[reason]
        self._update_game_feedback(config.GAME_TEXT['try_again']
                                   .format(player, reason))

    def announce_win(self, player):
        """Update feedback bar to announce that the game was won.

        Args:
            player (Player): The winner.
        """
        self._update_game_feedback(config.GAME_TEXT['win'].format(player))

    def announce_draw(self):
        """Update feedback bar to announce the the game ended in a draw."""

        self._update_game_feedback(config.GAME_TEXT['draw'])

    def _update_game_feedback(self, text):
        self.widgets['game_feedback'].configure(text=text)

    def update_square(self, color, position):
        """Paint a game square to reflect a color played in that position.

        Args:
            color (Color): The color that was played.
            position: A 2-tuple in format (row, column).
        """
        row, column = position
        color = config.COLOR_TO_TK[color]
        self.widgets['squares'][row][column].configure(bg=color)

    def flash_squares(self, positions):
        """Flash some of the game squares.

        Args:
            positions (set): A set of 2-tuples in format (row, column)
                of the positions to flash.
        """
        for row, column in positions:
            flash(element=self.widgets['squares'][row][column],
                  window=self.view.window, color=config.SQUARE_BACKGROUND)

    def reset_squares(self):
        """Recreate the game matrix to start a new game."""
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
