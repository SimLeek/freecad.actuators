from compiled_ui.planetary_ui import Ui_Dialog

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore
from search_planetaries import PlanetarySearchWorker

import math as m

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.computing = False

        self.ui.min_sun_teeth_spinbox.valueChanged.connect(self.on_min_sun_user_changed)
        self.ui.min_ring_teeth_spinbox.valueChanged.connect(self.on_min_ring_user_changed)
        self.ui.min_planet_teeth_spinbox.valueChanged.connect(self.on_min_planet_user_changed)
        self.ui.min_sun_teeth_spinbox_lock.lock_state_changed.connect(self.on_min_sun_lock_changed)
        self.ui.min_ring_teeth_spinbox_lock.lock_state_changed.connect(self.on_min_ring_lock_changed)
        self.ui.min_planet_teeth_spinbox_lock.lock_state_changed.connect(self.on_min_planet_lock_changed)

        self.ui.max_sun_teeth_spinbox.valueChanged.connect(self.on_max_sun_user_changed)
        self.ui.max_ring_teeth_spinbox.valueChanged.connect(self.on_max_ring_user_changed)
        self.ui.max_planet_teeth_spinbox.valueChanged.connect(self.on_max_planet_user_changed)
        self.ui.max_sun_teeth_spinbox_lock.lock_state_changed.connect(self.on_max_sun_lock_changed)
        self.ui.max_ring_teeth_spinbox_lock.lock_state_changed.connect(self.on_max_ring_lock_changed)
        self.ui.max_planet_teeth_spinbox_lock.lock_state_changed.connect(self.on_max_planet_lock_changed)

        self.ui.input_combobox.currentIndexChanged.connect(self.on_combobox_changed)
        self.ui.output_combobox.currentIndexChanged.connect(self.on_combobox_changed)
        self.ui.fixed_combobox.currentIndexChanged.connect(self.on_combobox_changed)

        self.ui.input_combobo_lock.lock_state_changed.connect(self.on_combobox_lock_changed)
        self.ui.output_combobox_lock.lock_state_changed.connect(self.on_combobox_lock_changed)
        self.ui.fixed_combobox_lock.lock_state_changed.connect(self.on_combobox_lock_changed)

        self.ui.min_module_lineedit.textChanged.connect(self.on_min_module_user_changed)
        self.ui.min_module_lineedit_lock.lock_state_changed.connect(self.on_min_module_lock_changed)
        self.ui.max_ring_diam_lineedit.textChanged.connect(self.on_max_ring_diam_user_changed)
        self.ui.max_ring_diam_lineedit_lock.lock_state_changed.connect(self.on_max_ring_diam_lock_changed)
        self.ui.min_circular_pitch_lineedit.textChanged.connect(self.on_min_circular_pitch_user_changed)

        self.ui.min_height_lineedit.textChanged.connect(self.on_min_height_user_changed)
        self.ui.min_height_lineedit_lock.lock_state_changed.connect(self.on_min_height_lock_changed)
        self.ui.max_height_lineedit.textChanged.connect(self.on_max_height_user_changed)
        self.ui.max_height_lineedit_lock.lock_state_changed.connect(self.on_max_height_lock_changed)

        self.ui.gear_addendum_lineedit.textChanged.connect(self.on_gear_addendum_user_changed)
        self.ui.gear_addendum_lineedit_lock.lock_state_changed.connect(self.on_gear_addendum_lock_changed)
        self.ui.planet_clearance_lineedit.textChanged.connect(self.on_planet_clearance_user_changed)
        self.ui.planet_clearance_lineedit_lock.lock_state_changed.connect(self.on_planet_clearance_lock_changed)

        self.planet_search_worker = None
        self.ui.gear_ratio_options_calculate.clicked.connect(self.start_planetary_search)
        self.ui.gear_ratio_options_abort.clicked.connect(self.abort_planetary_search)
        self.ui.gear_ratio_options_calculate.setEnabled(True)
        self.ui.gear_ratio_options_abort.setEnabled(False)

        self.ui.target_inverse_gear_ratio_lineedit.textChanged.connect(self.on_target_inverse_gear_ratio_lineedit_user_changed)
        self.ui.target_gear_ratio_lineedit.textChanged.connect(self.on_target_gear_ratio_lineedit_user_changed)

        self.reset_unlocked_comboboxes()

    def on_target_inverse_gear_ratio_lineedit_user_changed(self, _):
        if not self.computing:
            if self.ui.target_inverse_gear_ratio_lineedit.get_value()!=0:
                self.computing = True
                try:
                    self.ui.target_gear_ratio_lineedit.set_value(1/self.ui.target_inverse_gear_ratio_lineedit.get_value())
                finally:
                    self.computing = False
            self.ui.target_inverse_gear_ratio_lineedit_lock.is_locked = True

    def on_target_gear_ratio_lineedit_user_changed(self, _):
        if not self.computing:
            if self.ui.target_gear_ratio_lineedit.get_value()!=0:
                self.computing = True
                try:
                    self.ui.target_inverse_gear_ratio_lineedit.set_value(1/self.ui.target_gear_ratio_lineedit.get_value())
                finally:
                    self.computing = False
            self.ui.target_inverse_gear_ratio_lineedit_lock.is_locked = True

    def start_planetary_search(self):
        """Starts the long function in a worker thread."""
        circular_pitch = self.ui.min_circular_pitch_lineedit.get_mm_value()
        if circular_pitch==0:
            self.ui.gear_ratio_options_combobox.clear()
            self.ui.gear_ratio_options_combobox.addItems(["Set circular pitch to non-zero to avoid div-0"])
            return


        self.ui.gear_ratio_options_progress.setValue(0)
        self.planet_search_worker = PlanetarySearchWorker(
            self.ui.min_planet_teeth_spinbox.value(),
            self.ui.max_planet_teeth_spinbox.value(),
            self.ui.min_sun_teeth_spinbox.value(),
            self.ui.max_sun_teeth_spinbox.value(),
            self.ui.target_inverse_gear_ratio_lineedit.get_value(),
            self.ui.gear_addendum_lineedit.get_mm_value(),
            self.ui.planet_clearance_lineedit.get_mm_value(),
            self.ui.num_results_spinbox.value(),
            self.ui.number_of_planets_spinbox.value(),
            self.ui.min_circular_pitch_lineedit.get_mm_value(),
            self.ui.use_abs_checkbox.isChecked(),
            self.ui.fixed_combobox.currentText(),
            self.ui.input_combobox.currentText(),
            self.ui.output_combobox.currentText()
        )
        self.planet_search_worker.progress_updated.connect(self.ui.gear_ratio_options_progress.setValue)
        self.planet_search_worker.finished.connect(self.populate_results)
        self.planet_search_worker.start()
        self.ui.gear_ratio_options_calculate.setEnabled(False)
        self.ui.gear_ratio_options_abort.setEnabled(True)

    def abort_planetary_search(self):
        """Aborts the running function."""
        if self.planet_search_worker:
            self.planet_search_worker.abort()
            self.ui.gear_ratio_options_calculate.setEnabled(True)
            self.ui.gear_ratio_options_abort.setEnabled(False)

    def populate_results(self, results):
        """Populates the combo box with results."""
        self.ui.gear_ratio_options_combobox.clear()
        self.ui.gear_ratio_options_combobox.add_items(results)

        self.ui.gear_ratio_options_calculate.setEnabled(True)
        self.ui.gear_ratio_options_abort.setEnabled(False)

    # region min_planetary

    def recalculate_min_ring(self):
        sun_teeth = self.ui.min_sun_teeth_spinbox.value()
        planet_teeth = self.ui.min_planet_teeth_spinbox.value()
        ring_teeth = int(sun_teeth + 2 * planet_teeth)
        if self.ui.min_ring_teeth_spinbox_lock.is_locked:
            if self.ui.min_ring_teeth_spinbox.value() < ring_teeth:
                self.ui.min_ring_teeth_spinbox.setToolTip("Invalid min ring teeth. Ring teeth cannot be les than S+2P")
                self.ui.min_ring_teeth_spinbox.setStyleSheet("background-color: red;")
            else:
                self.ui.min_ring_teeth_spinbox.setStyleSheet("")
        else:
            self.ui.min_ring_teeth_spinbox.setStyleSheet("")
            self.computing = True
            try:
                self.ui.min_ring_teeth_spinbox.setValue(ring_teeth)
            finally:
                self.computing = False

    def recalculate_min_planets(self):
        sun_teeth = self.ui.min_sun_teeth_spinbox.value()
        ring_teeth = self.ui.min_ring_teeth_spinbox.value()
        planet_teeth = int((ring_teeth - sun_teeth) / 2)
        if self.ui.min_planet_teeth_spinbox_lock.is_locked:
            if self.ui.min_planet_teeth_spinbox.value() < planet_teeth:
                self.ui.min_planet_teeth_spinbox.setToolTip(
                    "Invalid min planet teeth. Planet teeth cannot be less than (R-S)/2")
                self.ui.min_planet_teeth_spinbox.setStyleSheet("background-color: red;")
            else:
                self.ui.min_planet_teeth_spinbox.setStyleSheet("")
        else:
            self.ui.min_planet_teeth_spinbox.setStyleSheet("")
            self.computing = True
            try:
                self.ui.min_planet_teeth_spinbox.setValue(planet_teeth)
            finally:
                self.computing = False

    def recalculate_min_sun(self):
        planet_teeth = self.ui.min_planet_teeth_spinbox.value()
        ring_teeth = self.ui.min_ring_teeth_spinbox.value()
        sun_teeth = int(ring_teeth - 2 * planet_teeth)
        if self.ui.min_sun_teeth_spinbox_lock.is_locked:
            if self.ui.min_sun_teeth_spinbox.value() < sun_teeth:
                self.ui.min_sun_teeth_spinbox.setToolTip("Invalid min sun teeth. Sun teeth cannot be les than R-2P")
                self.ui.min_sun_teeth_spinbox.setStyleSheet("background-color: red;")
            else:
                self.ui.min_sun_teeth_spinbox.setStyleSheet("")
        else:
            self.ui.min_sun_teeth_spinbox.setStyleSheet("")
            self.computing = True
            try:
                self.ui.min_sun_teeth_spinbox.setValue(sun_teeth)
            finally:
                self.computing = False

    def on_min_sun_lock_changed(self, _):
        if not self.ui.min_sun_teeth_spinbox_lock.is_locked:
            self.recalculate_min_sun()  # clear errors if any
        if self.ui.min_planet_teeth_spinbox_lock.is_locked:
            self.recalculate_min_ring()
        elif self.ui.min_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_min_planets()
        if self.ui.min_sun_teeth_spinbox_lock.is_locked:
            self.recalculate_min_sun()  # clear errors if any
        self.recalculate_max_ring()  # calculate max teeth given min sun, min planet, max ring diam, and min module

    def on_min_sun_user_changed(self, _):
        if not self.computing:
            self.ui.min_sun_teeth_spinbox_lock.is_locked = True

    def on_min_ring_lock_changed(self, _):
        if not self.ui.min_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_min_ring()  # we were unlocked, so calculate us first based on others
        if self.ui.min_planet_teeth_spinbox_lock.is_locked:
            self.recalculate_min_sun()
        elif self.ui.min_sun_teeth_spinbox_lock.is_locked:
            self.recalculate_min_planets()
        if self.ui.min_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_min_ring()  # we were locked, so clear errors that were fixed from others changing

    def on_min_ring_user_changed(self, _):
        if not self.computing:
            self.ui.min_ring_teeth_spinbox_lock.is_locked = True

    def on_min_planet_lock_changed(self, _):
        if not self.ui.min_planet_teeth_spinbox_lock.is_locked:
            self.recalculate_min_planets()  # clear errors if any
        if self.ui.min_sun_teeth_spinbox_lock.is_locked:
            self.recalculate_min_ring()
        elif self.ui.min_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_min_sun()
        if self.ui.min_planet_teeth_spinbox_lock.is_locked:
            self.recalculate_min_planets()  # clear errors if any
        self.recalculate_max_ring()  # calculate max teeth given min sun, min planet, max ring diam, and min module

    def on_min_planet_user_changed(self, _):
        if not self.computing:
            self.ui.min_planet_teeth_spinbox_lock.is_locked = True

    # endregion min_planetary

    # region max_planetary

    def recalculate_max_ring(self):
        if self.ui.max_ring_diam_lineedit_lock.is_locked and self.ui.min_module_lineedit_lock.is_locked and not self.ui.max_ring_teeth_spinbox_lock.is_locked:
            ring_diameter = self.ui.max_ring_diam_lineedit.get_mm_value()
            module = self.ui.min_module_lineedit.get_mm_value()
            if ring_diameter > 0 and module > 0:
                ring_teeth = int((ring_diameter / module) - 6)
                planet_teeth = int((ring_teeth-self.ui.min_sun_teeth_spinbox.value())/2)
                sun_teeth = int(ring_teeth-2*self.ui.min_planet_teeth_spinbox.value())
                self.computing = True
                try:
                    self.ui.max_ring_teeth_spinbox.setValue(ring_teeth)
                    self.ui.max_planet_teeth_spinbox.setValue(planet_teeth)
                    self.ui.max_sun_teeth_spinbox.setValue(sun_teeth)
                finally:
                    self.computing = False
        else:
            sun_teeth = self.ui.max_sun_teeth_spinbox.value()
            planet_teeth = self.ui.max_planet_teeth_spinbox.value()
            ring_teeth = int(sun_teeth + 2 * planet_teeth)
            if self.ui.max_ring_teeth_spinbox_lock.is_locked:
                if self.ui.max_ring_teeth_spinbox.value() > ring_teeth:
                    self.ui.max_ring_teeth_spinbox.setToolTip("Invalid max ring teeth. Ring teeth cannot be greater than S+2P")
                    self.ui.max_ring_teeth_spinbox.setStyleSheet("background-color: red;")
                else:
                    self.ui.max_ring_teeth_spinbox.setStyleSheet("")
            else:
                self.ui.max_ring_teeth_spinbox.setStyleSheet("")
                self.computing = True
                try:
                    self.ui.max_ring_teeth_spinbox.setValue(ring_teeth)
                finally:
                    self.computing = False

    def recalculate_max_planets(self):
        sun_teeth = self.ui.max_sun_teeth_spinbox.value()
        ring_teeth = self.ui.max_ring_teeth_spinbox.value()
        planet_teeth = int(m.ceil((ring_teeth - sun_teeth) / 2))
        if self.ui.max_planet_teeth_spinbox_lock.is_locked:
            if self.ui.max_planet_teeth_spinbox.value() > planet_teeth:
                self.ui.max_planet_teeth_spinbox.setToolTip(
                    "Invalid max planet teeth. Planet teeth cannot be greater than (R-S)/2")
                self.ui.max_planet_teeth_spinbox.setStyleSheet("background-color: red;")
            else:
                self.ui.max_planet_teeth_spinbox.setStyleSheet("")
        else:
            self.ui.max_planet_teeth_spinbox.setStyleSheet("")
            self.computing = True
            try:
                self.ui.max_planet_teeth_spinbox.setValue(planet_teeth)
            finally:
                self.computing = False

    def recalculate_max_sun(self):
        planet_teeth = self.ui.min_planet_teeth_spinbox.value()
        ring_teeth = self.ui.max_ring_teeth_spinbox.value()
        sun_teeth = int(ring_teeth - 2 * planet_teeth)
        if self.ui.max_sun_teeth_spinbox_lock.is_locked:
            if self.ui.max_sun_teeth_spinbox.value() > sun_teeth:
                self.ui.max_sun_teeth_spinbox.setToolTip("Invalid min sun teeth. Sun teeth cannot be les than R-2P")
                self.ui.max_sun_teeth_spinbox.setStyleSheet("background-color: red;")
            else:
                self.ui.max_sun_teeth_spinbox.setStyleSheet("")
        else:
            self.ui.max_sun_teeth_spinbox.setStyleSheet("")
            self.computing = True
            try:
                self.ui.max_sun_teeth_spinbox.setValue(sun_teeth)
            finally:
                self.computing = False

    def on_max_sun_lock_changed(self, _):
        if not self.ui.max_sun_teeth_spinbox_lock.is_locked:
            self.recalculate_max_sun()  # clear errors if any
        if self.ui.max_planet_teeth_spinbox_lock.is_locked:
            self.recalculate_max_ring()
        elif self.ui.max_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_max_planets()
        if self.ui.max_sun_teeth_spinbox_lock.is_locked:
            self.recalculate_max_sun()  # clear errors if any

    def on_max_sun_user_changed(self, _):
        if not self.computing:
            self.ui.max_sun_teeth_spinbox_lock.is_locked = True

    def on_max_ring_lock_changed(self, _):
        if not self.ui.max_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_max_ring()  # we were unlocked, so calculate us first based on others
        if self.ui.max_planet_teeth_spinbox_lock.is_locked:
            self.recalculate_max_sun()
        elif self.ui.max_sun_teeth_spinbox_lock.is_locked:
            self.recalculate_max_planets()
        if self.ui.max_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_max_ring()  # we were locked, so clear errors that were fixed from others changing

    def on_max_ring_user_changed(self, _):
        if not self.computing:
            self.ui.max_ring_teeth_spinbox_lock.is_locked = True

    def on_max_planet_lock_changed(self, _):
        if not self.ui.max_planet_teeth_spinbox_lock.is_locked:
            self.recalculate_max_planets()  # clear errors if any
        if self.ui.max_sun_teeth_spinbox_lock.is_locked:
            self.recalculate_max_ring()
        elif self.ui.max_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_max_sun()
        if self.ui.max_planet_teeth_spinbox_lock.is_locked:
            self.recalculate_max_planets()  # clear errors if any

    def on_max_planet_user_changed(self, _):
        if not self.computing:
            self.ui.max_planet_teeth_spinbox_lock.is_locked = True

    # endregion max_planetary

    # region input_output_fixed

    def get_locked_values(self):
        """Returns a dictionary of locked combobox values."""
        locked_values = {}
        if self.ui.input_combobo_lock.is_locked:
            locked_values["input"] = self.ui.input_combobox.currentText()
        if self.ui.output_combobox_lock.is_locked:
            locked_values["output"] = self.ui.output_combobox.currentText()
        if self.ui.fixed_combobox_lock.is_locked:
            locked_values["fixed"] = self.ui.fixed_combobox.currentText()
        return locked_values

    def reset_unlocked_comboboxes(self):
        """Sets unlocked comboboxes to 'Any' by default."""
        self.computing = True
        try:
            if not self.ui.input_combobo_lock.is_locked:
                self.ui.input_combobox.setCurrentText("Any")
            if not self.ui.output_combobox_lock.is_locked:
                self.ui.output_combobox.setCurrentText("Any")
            if not self.ui.fixed_combobox_lock.is_locked:
                self.ui.fixed_combobox.setCurrentText("Any")
        finally:
            self.computing = False

    def determine_remaining_value(self):
        """Determines and sets the correct value for an unlocked combobox if two are locked."""
        locked_values = self.get_locked_values()
        all_options = {"Sun", "Ring", "Carrier"}

        if len(locked_values) == 2:  # If two are locked, set the remaining one
            used_values = set(locked_values.values())
            remaining_value = (all_options - used_values).pop()  # The only remaining valid option

            self.computing = True
            try:
                if not self.ui.input_combobo_lock.is_locked:
                    self.ui.input_combobox.setCurrentText(remaining_value)
                elif not self.ui.output_combobox_lock.is_locked:
                    self.ui.output_combobox.setCurrentText(remaining_value)
                elif not self.ui.fixed_combobox_lock.is_locked:
                    self.ui.fixed_combobox.setCurrentText(remaining_value)
            finally:
                self.computing = False

        elif len(locked_values) < 2:  # If fewer than 2 are locked, reset unlocked ones to 'Any'
            self.reset_unlocked_comboboxes()

    def on_combobox_changed(self, _):
        """Triggered when a combobox value is changed manually."""
        if not self.computing:
            sender = self.sender()
            if sender == self.ui.input_combobox:
                self.ui.input_combobo_lock.is_locked = True
            elif sender == self.ui.output_combobox:
                self.ui.output_combobox_lock.is_locked = True
            elif sender == self.ui.fixed_combobox:
                self.ui.fixed_combobox_lock.is_locked = True

            self.determine_remaining_value()

    def on_combobox_lock_changed(self, _):
        """Triggered when a combobox lock state is changed."""
        self.determine_remaining_value()

    # endregion input_output_fixed

    # region module_and_diam

    def on_min_module_lock_changed(self, _):
        if not self.ui.max_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_max_ring()
        if not self.ui.gear_addendum_lineedit_lock.is_locked:
            self.recalculate_gear_addendum()
        if not self.ui.planet_clearance_lineedit_lock.is_locked:
            self.recalculate_planet_clearance()

    def on_min_module_user_changed(self, _):
        if not self.computing:
            if self.ui.min_module_lineedit.get_mm_value()!=0.0:
                self.computing = True
                try:
                    self.ui.min_circular_pitch_lineedit.set_mm_value(self.ui.min_module_lineedit.get_mm_value()*m.pi)
                finally:
                    self.computing = False
            self.ui.min_module_lineedit_lock.is_locked = True

    def on_min_circular_pitch_user_changed(self, _):
        if not self.computing:
            if self.ui.min_circular_pitch_lineedit.get_mm_value()!=0.0:
                self.computing = True
                try:
                    self.ui.min_module_lineedit.set_mm_value(self.ui.min_circular_pitch_lineedit.get_mm_value()/m.pi)
                finally:
                    self.computing = False
            self.ui.min_module_lineedit_lock.is_locked = True

    def on_max_ring_diam_lock_changed(self, _):
        if not self.ui.max_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_max_ring()

    def on_max_ring_diam_user_changed(self, _):
        if not self.computing:
            self.ui.max_ring_diam_lineedit_lock.is_locked = True

    # endregion module_and_diam

    # region min_max_height

    def on_min_height_lock_changed(self, _):
        if self.ui.max_height_lineedit.get_mm_value()<self.ui.min_height_lineedit.get_mm_value():
            if self.ui.max_height_lineedit_lock.is_locked:
                self.ui.max_height_lineedit.setToolTip("Invalid max height. Max height cannot be less than min height.")
                self.ui.max_height_lineedit.setStyleSheet("background-color: red;")
            else:
                self.computing = True
                try:
                    self.ui.max_height_lineedit.set_mm_value(self.ui.min_height_lineedit.get_mm_value())
                    self.ui.max_height_lineedit.setToolTip("")
                    self.ui.max_height_lineedit.setStyleSheet("")
                finally:
                    self.computing = False
        else:
            self.ui.max_height_lineedit.setToolTip("")
            self.ui.max_height_lineedit.setStyleSheet("")

    def on_max_height_lock_changed(self, _):
        if self.ui.max_height_lineedit.get_mm_value()<self.ui.min_height_lineedit.get_mm_value():
            if self.ui.min_height_lineedit_lock.is_locked:
                self.ui.min_height_lineedit.setToolTip("Invalid min height. Min height cannot be greater than max height.")
                self.ui.min_height_lineedit.setStyleSheet("background-color: red;")
            else:
                self.computing = True
                try:
                    self.ui.min_height_lineedit.set_mm_value(self.ui.max_height_lineedit.get_mm_value())
                    self.ui.min_height_lineedit.setToolTip("")
                    self.ui.min_height_lineedit.setStyleSheet("")
                finally:
                    self.computing = False
        else:
            self.ui.min_height_lineedit.setToolTip("")
            self.ui.min_height_lineedit.setStyleSheet("")

    def on_min_height_user_changed(self, _):
        if not self.computing:
            self.ui.min_height_lineedit_lock.is_locked = True

    def on_max_height_user_changed(self, _):
        if not self.computing:
            self.ui.max_height_lineedit_lock.is_locked = True

    # endregion

    # region addendum and clearnace
    def recalculate_gear_addendum(self):
        if not self.ui.gear_addendum_lineedit_lock.is_locked:
            self.computing = True
            try:
                if self.ui.actual_module_lineedit.get_mm_value()!=0:
                    self.ui.gear_addendum_lineedit.set_mm_value(self.ui.actual_module_lineedit.get_mm_value())
                elif self.ui.min_module_lineedit.get_mm_value()!=0:
                    self.ui.gear_addendum_lineedit.set_mm_value(self.ui.min_module_lineedit.get_mm_value())
            finally:
                self.computing = False

    def recalculate_planet_clearance(self):
        if not self.ui.planet_clearance_lineedit_lock.is_locked:
            self.computing = True
            try:
                if self.ui.actual_module_lineedit.get_mm_value()!=0:
                    self.ui.planet_clearance_lineedit.set_mm_value(self.ui.actual_module_lineedit.get_mm_value()/2.0)
                elif self.ui.min_module_lineedit.get_mm_value()!=0:
                    self.ui.planet_clearance_lineedit.set_mm_value(self.ui.min_module_lineedit.get_mm_value()/2.0)
            finally:
                self.computing = False

    def on_gear_addendum_user_changed(self):
        if not self.computing:
            self.ui.gear_addendum_lineedit_lock.is_locked = True

    def on_gear_addendum_lock_changed(self):
        self.recalculate_gear_addendum()

    def on_planet_clearance_user_changed(self):
        if not self.computing:
            self.ui.planet_clearance_lineedit_lock.is_locked = True

    def on_planet_clearance_lock_changed(self):
        self.recalculate_planet_clearance()

    # endregion



import sys

app = QApplication(sys.argv)
dialog = MyDialog()
dialog.show()
sys.exit(app.exec_())
