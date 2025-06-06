"""
Main window and state management for the BLDC Motor Stator Visualization.
"""
import sys
from PySide2.QtWidgets import QApplication, QDialog, QWidget, QVBoxLayout
from visualization_drawing import draw_axle, draw_magnets, draw_outrunner, draw_stator_core
from wire_drawing import draw_wires
from stator_visualization_setup import connect_display_checkboxes, connect_display_and_parameters, update_visualization, update_visualization_with_cache
from defaults import connect_defaults
from freecad.actuators.compiled_ui.bldc_ui import Ui_BLDCDialog
from slot_pole_grid import connect_slot_pole

class BLDCWindow(QDialog):
    """A window for visualizing BLDC motor stator with interactive controls."""
    def __init__(self):
        """Initialize the BLDC motor visualization window."""
        super().__init__()

        self.use_cache = False
        self.calculating = False

        self.ui = Ui_BLDCDialog()
        self.ui.setupUi(self)

        # Assign callback functions
        self.draw_axle_callback = draw_axle
        self.draw_magnets_callback = draw_magnets
        self.draw_outrunner_callback = draw_outrunner
        self.draw_stator_core_callback = draw_stator_core
        self.draw_wires_callback = draw_wires

        # Setup UI
        connect_display_checkboxes(self)
        connect_display_and_parameters(self)
        connect_defaults(self)
        connect_slot_pole(self)

        # Connect range changed signal
        self.ui.stator_plot_widget.sigRangeChanged.connect(lambda: update_visualization_with_cache(self))

        # Initial draw
        self.update_visualization = update_visualization
        #update_visualization_with_cache(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BLDCWindow()
    window.show()
    sys.exit(app.exec_())