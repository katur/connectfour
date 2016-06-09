from board import Board
from player import Player

DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7
DEFAULT_TO_WIN = 4


class ConnectFour(object):
    """
    A Connect Four model, complete with a Board and Players.

    This session also broadcasts game events to Listeners.
    """

    def __init__(self, num_rows=DEFAULT_ROWS, num_columns=DEFAULT_COLUMNS,
                 num_to_win=DEFAULT_TO_WIN):
        if num_rows < 1 or num_columns < 1:
            raise ValueError('Row and column dimensions must be at least 1')

        if (num_to_win < 1 or
                (num_to_win > num_rows and num_to_win > num_columns)):
            raise ValueError('Number to win must be at least 1, and '
                             'cannot exceed both the number of rows '
                             'and the number of columns')

        self.board = Board(num_rows, num_columns, num_to_win)
        self.session_started = False
        self.game_started = False
        self.game_number = 0
        self.listeners = []
        self.players = []

        # Which player goes first in the next game
        self.first_turn_index = 0

        # Which player goes next in the current game
        self.current_player_index = 0

    def __str__(self):
        return 'ConnectFour [board:{}, num_players:{}]'.format(
            self.board, self.get_number_of_players())

    def __repr__(self):
        return self.__str__()

    def add_listener(self, listener):
        """
        Add a listener to receive events made by this model.

        Exits silently if listener is already subscribed.
        """
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener):
        """
        Remove a listener from receiving events made by this model.

        Exits silently if listener was not subscribed.
        """
        if listener in self.listeners:
            self.listeners.remove(listener)

    #####################
    # Game play methods #
    #####################

    def add_player(self, name, color):
        """
        Add a player to the session.
        """
        if self.session_started:
            raise RuntimeError('Cannot add player before session started')

        player = Player(name, color)
        self.players.append(player)
        self.fire_player_added_event(player)

    def start_game(self):
        """
        Start a game.
        """
        if self.game_started:
            raise RuntimeError('Cannot start game while another game '
                               'is in progress')
        if not self.players:
            raise RuntimeError('Cannot start game with no players')

        self.board.reset()
        self.session_started = True
        self.game_started = True
        self.game_number += 1
        self.fire_game_started_event(self.game_number)

        self.current_player_index = self.first_turn_index

        # Prepare first_turn_index for the next game
        self.first_turn_index = ((self.first_turn_index + 1)
                                 % self.get_number_of_players())

        self.fire_next_player_event(self.get_current_player())

    def play_disc(self, column):
        """
        Play a disc in a column.

        Assumes the disc is played by the current player.
        """
        if not self.game_started:
            raise RuntimeError('Cannot play disc before game is started')

        if not self.board.is_column_in_bounds(column):
            self.fire_try_again_event('Column is out of bounds')

        elif self.board.is_column_full(column):
            self.fire_try_again_event('Column is full')

        else:
            self.process_play(column)
            # TODO: could instead have listeners respond that render complete

    def process_play(self, column):
        """
        Helper function to play a chip
        """
        player = self.get_current_player()
        row = self.board.add_disc(player.disc, column)
        self.fire_disc_played_event(player, (row, column))

        winning_positions = self.board.get_winning_positions((row, column))

        if winning_positions:
            self.process_win(player, winning_positions)
        elif self.board.is_full():
            self.process_draw()
        else:
            self.process_next_player()

    def process_win(self, player, winning_positions):
        self.game_started = False
        player.number_of_wins += 1
        self.fire_game_won_event(player, winning_positions)

    def process_draw(self):
        self.game_started = False
        self.fire_game_draw_event()

    def process_next_player(self):
        self.current_player_index = ((self.current_player_index + 1)
                                     % self.get_number_of_players())

        self.fire_next_player_event(self.get_current_player())

    ############################
    # Fire events to listeners #
    ############################

    def fire_player_added_event(self, player):
        """
        Alert listeners that a player was added.
        """
        for listener in self.listeners:
            listener.player_added(player)

    def fire_game_started_event(self, game_number):
        """
        Alert listeners that a game was started.
        """
        for listener in self.listeners:
            listener.game_started(game_number)

    def fire_next_player_event(self, player):
        """
        Alert listeners who the next player is.
        """
        for listener in self.listeners:
            listener.next_player(player)

    def fire_try_again_event(self, player, reason):
        """
        Alert listeners that player should try again, because of reason.
        """
        for listener in self.listeners:
            listener.try_again(player, reason)

    def fire_disc_played_event(self, player, position):
        """
        Alert listeners that a disc was played by player at position.
        """
        for listener in self.listeners:
            listener.disc_played(player, position)

    def fire_game_won_event(self, player, winning_positions):
        """
        Alert listeners that game was won by player.
        """
        for listener in self.listeners:
            listener.game_won(player, winning_positions)

    def fire_game_draw_event(self):
        """
        Alert listeners that game ended in a draw.
        """
        for listener in self.listeners:
            listener.game_draw()

    ##################
    # Simple helpers #
    ##################

    def get_number_of_players(self):
        return len(self.players)

    def get_player(self, index):
        if index < 0 or index >= self.get_number_of_players():
            raise IndexError('Player index {} is out of bounds'.format(index))
        return self.players[index]

    def get_current_player(self):
        if not self.players:
            raise RuntimeError('Cannot get current player if no '
                               'players have been added yet')
        return self.players[self.current_player_index]
