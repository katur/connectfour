from connectfour.views.gui.config import (
    FLASH_CYCLES, FLASH_CYCLE_TIME, FLASH_WAIT_TIME)


def get_positive_int(num, name='Number', max_value=None):
    """Convert num to an int.

    Raises an error if num is not convertible to a positive int.

    Args:
        num (str): The value to cast to an int.
        name (Optional[str]): The name of num (e.g. 'Days'), to print in
            error messages.
        max_value (Optional[int]): Maximum value for num.
    Returns:
        int: The num cast to an int, if meets criteria.
    Raises:
        ValueError: If num is not convertible to an int; if num is not
            positive; or if num exceeds max_value.
    """
    try:
        num = int(num)
    except ValueError:
        raise ValueError('{} must be convertible to integer'.format(name))

    if num <= 0:
        raise ValueError('{} must be positive'.format(name))

    if max_value and num > max_value:
        raise ValueError("{} can't exceed {}".format(name, max_value))

    return num


def flash(window, element, color, num_cycles=FLASH_CYCLES,
          cycle_time=FLASH_CYCLE_TIME, wait_time=FLASH_WAIT_TIME):
    """Make an element in window flash a certain color.

    Flashing is between color and the element's original color. After
    flashing ceases, element will be its original color.

    Any errors raised while changing element color are ignored. So,
    it is okay to destroying elements while they are still flashing.

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

    def _set_color(element, color):
        """Set element to color, ignoring errors."""
        try:
            element.config(bg=color)
        except Exception:
            pass

    for i in range(num_cycles):
        window.after(wait_time + cycle_time * i,
                     lambda: _set_color(element, color))
        window.after(int(wait_time + cycle_time * (i + 0.5)),
                     lambda: _set_color(element, original_color))
