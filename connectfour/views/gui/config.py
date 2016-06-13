from connectfour.config import Color, TryAgainReason


COLOR_TO_TK = {
    Color.black: 'Black',
    Color.red: 'Red',
    Color.blue: 'Blue',
    Color.purple: 'Purple',
    Color.orange: 'Orange',
    Color.green: 'Green',
    Color.pink: 'PeachPuff',
    Color.dark_green: 'DarkGreen',
    Color.brown: 'Brown',
    Color.gray: 'Gray',
}

REASON_TO_STR = {
    TryAgainReason.column_out_of_bounds: 'out of bounds',
    TryAgainReason.column_full: 'column full',
}

PAD = 20

SQUARE_BACKGROUND = 'Yellow'
SQUARE_SIZE = 60
SQUARE_BORDER_WIDTH = 5

FLASH_CYCLES = 10
FLASH_CYCLE_TIME = 1000
FLASH_WAIT_TIME = 500

WINDOW_TITLE = 'Connect Four'

SETUP_TEXT = {
    'title': ('Welcome to Connect Four! Please select '
              'game parameters and add players.'),
    'rows': 'Rows:',
    'columns': 'Columns:',
    'to_win': 'To Win:',
    'add_player': 'Add Player',
    'feedback': 'Welcome, {0}\nTotal players added: {1}',
    'launch': 'Start Game',
    'quit': 'Exit',
}

GAME_TEXT = {
    'title': 'Welcome to Connect Four!',
    'play': 'Play',
    'next_player': "{0}'s turn",
    'try_again': '{0} try again ({1})',
    'win': '{0} won the round',
    'draw': 'Round ended in a draw',
    'play_again': 'Play Again',
    'quit': 'Exit',
}
