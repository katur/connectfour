from config import FLASH_CYCLES, FLASH_CYCLE_TIME, FLASH_WAIT_TIME


def _set_color(element, color):
    """Set element to color.

    Ignores any exceptions thrown. This is so that elements
    can be safely destroyed, even while flashing.
    """
    try:
        element.config(bg=color)
    except Exception:
        pass


def flash(window, element, color, num_cycles=FLASH_CYCLES,
          cycle_time=FLASH_CYCLE_TIME, wait_time=FLASH_WAIT_TIME):
    """Make element in window flash a certain color.

    Args:
        color: flashes between this color and its original color
    """
    original_color = element['bg']

    for i in range(num_cycles):
        window.after(wait_time + cycle_time * i,
                     lambda: _set_color(element, color))
        window.after(int(wait_time + cycle_time * (i + 0.5)),
                     lambda: _set_color(element, original_color))
