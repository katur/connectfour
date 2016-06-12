from connectfour.util.color import Color
from connectfour.util.tryagainreason import TryAgainReason


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
    TryAgainReason.column_out_of_bounds: 'Out of bounds',
    TryAgainReason.column_full: 'Column full',
}

WINDOW_TITLE_TEXT = 'Connect Four'
GAME_TITLE_TEXT = 'Welcome to Connect Four!'
SETUP_TITLE_TEXT = (
    'Welcome to Connect Four! '
    'Please select game parameters and add players.'
)


ADD_PLAYER_TEXT = 'Add Player'
LAUNCH_GAME_TEXT = 'Start Game'
PLAY_AGAIN_TEXT = 'Play Again'
COLUMN_TEXT = 'Play'
QUIT_TEXT = 'Exit'

PLAYER_FEEDBACK_TEXT = (
    'Welcome, {0}\n'
    'Total players added: {1}'
)

SQUARE_BACKGROUND = 'Yellow'
SQUARE_SIZE = 50
SQUARE_BORDER_WIDTH = 5

FLASH_CYCLES = 10
FLASH_CYCLE_TIME = 1000
FLASH_WAIT_TIME = 500

PAD = 20
