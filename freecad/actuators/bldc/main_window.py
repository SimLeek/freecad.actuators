"""
Main window and state management for the BLDC Motor Stator Visualization.
"""
import sys
from PySide2.QtWidgets import QApplication, QDialog, QWidget, QVBoxLayout
from top_view_visualization_drawing import draw_axle, draw_magnets, draw_outrunner, draw_stator_core
from wire_drawing import draw_wires
from top_view_visualization_setup import connect_display_checkboxes, connect_display_and_parameters, update_visualization, update_visualization_with_cache
from freecad.actuators.compiled_ui.bldc_ui import Ui_BLDCDialog
from slot_pole_grid import connect_slot_pole
from serialize import serialize, deserialize, connect_serialization_buttons
from side_view_visualization_drawing import draw_side_axle, draw_side_magnets, draw_side_outrunner, draw_side_stator, draw_side_wires, draw_side_base
from side_view_visualization_setup import connect_side_display_and_parameters, connect_side_display_checkboxes

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

        # draw side
        self.draw_side_axle_callback = draw_side_axle
        self.draw_side_magnets_callback = draw_side_magnets
        self.draw_side_outrunner_callback = draw_side_outrunner
        self.draw_side_stator_callback = draw_side_stator
        self.draw_side_wires_callback = draw_side_wires
        self.draw_side_base_callback = draw_side_base

        # Setup UI
        connect_display_checkboxes(self)
        connect_display_and_parameters(self)
        connect_slot_pole(self)
        connect_side_display_checkboxes(self)
        connect_side_display_and_parameters(self)

        # Initial draw
        self.update_visualization = update_visualization

        #update_visualization_with_cache(self)

        # ser/deser
        self.serialize = lambda : serialize(self)
        connect_serialization_buttons(self)

    @classmethod
    def deserialize(cls, data):
        instance = cls()
        return deserialize(instance, data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BLDCWindow()
    window.show()
    sys.exit(app.exec_())