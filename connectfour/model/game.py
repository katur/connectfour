from enum import Enum

from board import Board
from color import Color
from player import Player

DEFAULT_ROWS = 6
DEFAULT_COLUMNS = 7
DEFAULT_TO_WIN = 4


class TryAgainReason(Enum):
    """Reason that a player needs to try again.

    They need to try again if their previous move was illegal.
    """

    column_out_of_bounds = 1
    column_full = 2


class Game(object):
    """Top-level model of the Connect Four game."""

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
        self.session_in_progress = False
        self.round_in_progress = False
        self.round_number = 0
        self.listeners = []
        self.players = []

        # Which player goes first in the next round
        self.first_turn_index = 0

        # Which player goes next in the current round
        self.current_player_index = 0

    def __str__(self):
        return 'Game [board:{}, num_players:{}]'.format(
            self.board, self.get_num_players())

    def __repr__(self):
        return self.__str__()

    def add_listener(self, listener):
        """Add a listener to receive events made by this model.

        Exits silently if listener is already subscribed.
        """
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener):
        """Remove a listener from receiving events made by this model.

        Exits silently if listener was not subscribed.
        """
        if listener in self.listeners:
            self.listeners.remove(listener)

    #####################
    # Game play methods #
    #####################

    def add_player(self, name, color):
        """Add a player to the session."""
        if self.session_in_progress:
            raise RuntimeError('Cannot add player before session started')

        used_colors = self.get_used_colors()

        if len(used_colors) >= len(Color):
            raise RuntimeError('Game has reached max players')

        if color in used_colors:
            raise ValueError('Color {} is already taken'.format(color))

        player = Player(name, color)
        self.players.append(player)
        self._fire_player_added_event(player)

    def start_round(self):
        """Start a new round of the game."""
        if self.round_in_progress:
            raise RuntimeError('Cannot start a round while another '
                               'is in progress')
        if not self.players:
            raise RuntimeError('Cannot start a round with no players')

        self.board.reset()
        self.session_in_progress = True
        self.round_in_progress = True
        self.round_number += 1
        self._fire_round_started_event(self.round_number)

        self.current_player_index = self.first_turn_index

        # Prep first_turn_index for the next round
        self.first_turn_index = ((self.first_turn_index + 1)
                                 % self.get_num_players())

        self._fire_next_player_event(self.get_current_player())

    def play_disc(self, column):
        """Play a disc in a column.

        Assumes the disc is played by the current player.
        """
        if not self.round_in_progress:
            raise RuntimeError('Cannot play disc before round has started')

        if not self.board.is_column_in_bounds(column):
            self._fire_try_again_event(TryAgainReason.column_out_of_bounds)

        elif self.board.is_column_full(column):
            self._fire_try_again_event(TryAgainReason.column_full)

        else:
            self._process_play(column)
            # TODO: could instead have listeners respond that render complete

    ##########################
    # Helpers to play_disc() #
    ##########################

    def _process_play(self, column):
        player = self.get_current_player()
        row = self.board.add_disc(player.disc, column)
        self._fire_disc_played_event(player, (row, column))

        winning_positions = self.board.get_winning_positions((row, column))

        if winning_positions:
            self._process_win(player, winning_positions)
        elif self.board.is_full():
            self._process_draw()
        else:
            self._process_next_player()

    def _process_win(self, player, winning_positions):
        self.round_in_progress = False
        player.number_of_wins += 1
        self._fire_round_won_event(player, winning_positions)

    def _process_draw(self):
        self.round_in_progress = False
        self._fire_round_draw_event()

    def _process_next_player(self):
        self.current_player_index = ((self.current_player_index + 1)
                                     % self.get_num_players())

        self._fire_next_player_event(self.get_current_player())

    ############################
    # Fire events to listeners #
    ############################

    def _fire_player_added_event(self, player):
        """Alert listeners that a player was added."""
        for listener in self.listeners:
            listener.player_added(player)

    def _fire_round_started_event(self, round_number):
        """Alert listeners that a round was started."""
        for listener in self.listeners:
            listener.round_started(round_number)

    def _fire_next_player_event(self, player):
        """Alert listeners who the next player is."""
        for listener in self.listeners:
            listener.next_player(player)

    def _fire_try_again_event(self, player, reason):
        """Alert listeners that player should try again."""
        for listener in self.listeners:
            listener.try_again(player, reason)

    def _fire_disc_played_event(self, player, position):
        """Alert listeners that a disc was played by player at position."""
        for listener in self.listeners:
            listener.disc_played(player, position)

    def _fire_round_won_event(self, player, winning_positions):
        """Alert listeners that round was won by player."""
        for listener in self.listeners:
            listener.round_won(player, winning_positions)

    def _fire_round_draw_event(self):
        """Alert listeners that round ended in a draw."""
        for listener in self.listeners:
            listener.round_draw()

    ##################
    # Simple getters #
    ##################

    def get_current_player(self):
        if not self.players:
            raise RuntimeError('Cannot get current player if no '
                               'players have been added yet')
        return self.players[self.current_player_index]

    def get_player(self, index):
        if index < 0 or index >= self.get_num_players():
            raise IndexError('Player index {} is out of bounds'.format(index))
        return self.players[index]

    def get_num_players(self):
        return len(self.players)

    def get_used_colors(self):
        return {player.disc.color for player in self.players}

    def get_remaining_colors(self):
        return set(Color) - self.get_used_colors()

    def get_num_rows(self):
        return self.board.num_rows

    def get_num_columns(self):
        return self.board.num_columns


if __name__ == '__main__':
    game = Game(6, 7, 4)
    game.add_player('a', Color.red)
    game.add_player('b', Color.blue)
    game.add_player('c', Color.yellow)
    print game.get_remaining_colors()
