from connectfour.config import ConnectFourColor, TryAgainReason


MAX_NAME_LENGTH = 50
MAX_ROWS = 10
MAX_COLUMNS = 20
MAX_TO_WIN = 20
PAD = 20

COLOR_TO_TK = {
    ConnectFourColor.black: 'Black',
    ConnectFourColor.red: 'Red',
    ConnectFourColor.blue: 'Blue',
    ConnectFourColor.purple: 'Purple',
    ConnectFourColor.orange: 'Orange',
    ConnectFourColor.green: 'Green',
    ConnectFourColor.pink: 'PeachPuff',
    ConnectFourColor.dark_green: 'DarkGreen',
    ConnectFourColor.brown: 'Brown',
    ConnectFourColor.gray: 'Gray',
}

REASON_TO_STR = {
    TryAgainReason.column_out_of_bounds: 'out of bounds',
    TryAgainReason.column_full: 'column full',
}

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
    'title': 'Try to connect {0} in a row!',
    'play': 'Play',
    'next_player': "{0}'s turn",
    'try_again': '{0} try again ({1})',
    'win': '{0} won the round',
    'draw': 'Round ended in a draw',
    'play_again': 'Play Again',
    'quit': 'Exit',
}
