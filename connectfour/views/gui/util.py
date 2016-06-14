from config import FLASH_CYCLES, FLASH_CYCLE_TIME, FLASH_WAIT_TIME


def _set_color(element, color):
    """Set an element's background color, ignoring exceptions raised.

    Args:
        element: A Tkinter element.
        color: Color to set the background to. Can be any color format
            accepted by Tkinter.
    """
    try:
        element.config(bg=color)
    except Exception:
        pass


def flash(window, element, color, num_cycles=FLASH_CYCLES,
          cycle_time=FLASH_CYCLE_TIME, wait_time=FLASH_WAIT_TIME):
    """Make an element in window flash a certain color.

    Flashing is between color and the element's original color. After
    flashing ceases, element will be its original color.

    Destroying elements while they are still flashing is okay, since
    any exceptions raised when setting the color are caught and ignored.

    Args:
        window: A root Tkinter widget, to which timer events are added.
        element: The Tkinter element to flash.
        color: The flashing will be between this color and the element's
            original color. Can be any color format accepted by Tkinter.
        num_cycles (Optional[int]): How many times to flash the new color.
        cycle_time (Optional[int]): Duration in ms of one full flash cycle
            (the new color and original color each take a half cycle).
        wait_time(Optional[int]): Time in ms to wait before starting to flash.
    """
    original_color = element['bg']

    for i in range(num_cycles):
        window.after(wait_time + cycle_time * i,
                     lambda: _set_color(element, color))
        window.after(int(wait_time + cycle_time * (i + 0.5)),
                     lambda: _set_color(element, original_color))
