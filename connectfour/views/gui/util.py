from config import FLASH_CYCLES, FLASH_CYCLE_TIME, FLASH_WAIT_TIME


def flash(window, element, color, num_cycles=FLASH_CYCLES):
    """Make element in window flash.

    Args:
        color: flashes between this color and its original color
        num_cycles: how many times to flash each color


    Flashes between color and its original color.
    """
    original_color = element['bg']

    for i in range(num_cycles):
        window.after(
            FLASH_WAIT_TIME + FLASH_CYCLE_TIME * i,
            lambda: element.config(bg=color))
        window.after(
            int(FLASH_WAIT_TIME + FLASH_CYCLE_TIME * (i + 0.5)),
            lambda: element.config(bg=original_color))
