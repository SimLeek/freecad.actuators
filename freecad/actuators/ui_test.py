from compiled_ui.planetary_ui import Ui_Dialog

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

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
            self.ui.min_ring_teeth_spinbox.setValue(ring_teeth)
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
            self.ui.min_planet_teeth_spinbox.setValue(planet_teeth)
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
            self.ui.min_sun_teeth_spinbox.setValue(sun_teeth)
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

    def on_min_planet_user_changed(self, _):
        if not self.computing:
            self.ui.min_planet_teeth_spinbox_lock.is_locked = True

    # endregion min_planetary

    # region max_planetary

    def recalculate_max_ring(self):
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
            self.ui.max_ring_teeth_spinbox.setValue(ring_teeth)
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
            self.ui.max_planet_teeth_spinbox.setValue(planet_teeth)
            self.computing = False

    def recalculate_max_sun(self):
        planet_teeth = self.ui.max_planet_teeth_spinbox.value()
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
            self.ui.max_sun_teeth_spinbox.setValue(sun_teeth)
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


import sys

app = QApplication(sys.argv)
dialog = MyDialog()
dialog.show()
sys.exit(app.exec_())
