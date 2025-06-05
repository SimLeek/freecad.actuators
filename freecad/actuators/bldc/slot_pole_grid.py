"""
UI and visualization management functions for the BLDC Motor Stator Visualization.
"""

# stop potential import loops
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import BLDCWindow
else:
    from typing import Any
    BLDCWindow = Any

def connect_slot_pole(bldc_window: BLDCWindow):
    """Create horizontal Display Options group at the top."""
    bldc_window.slot_pole_validation = SlotPoleValidation(bldc_window)
    bldc_window.ui.slot_pole_grid_widget.set_callback(bldc_window.slot_pole_validation.slot_pole_cell_callback)

    bldc_window.ui.slot_pole_grid_widget.on_selection_changed.connect(lambda: update_lineedits)
    bldc_window.ui.num_slots_lineedit.changeEvent.connect(lambda: update_grid)
    bldc_window.ui.num_magnets_lineedit.changeEvent.connect(lambda: update_grid)

class SlotPoleValidation(object):
    def __init__(self, window):
        self.window = window

    def slot_pole_cell_callback(x, y):
        selectable = (x + y) % 2 != 0  # Selectable if x + y is odd
        if (x + y) % 3 == 0:
            text = f"[{x},{y}]"
            bg_color = QColor('lightblue')
        elif (x + y) % 3 == 1:
            text = f"({x},{y})"
            bg_color = QColor('lightgreen')
        else:
            text = f"{x},{y}"
            bg_color = None
        return selectable, text, bg_color
