# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gear-selectorssYjnjI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.16
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from .lock_button_ui import LockUnlockButton


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(451, 564)
        self.toolBox = QToolBox(Dialog)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setGeometry(QRect(10, 20, 431, 531))
        self.min_max_teeth_page = QWidget()
        self.min_max_teeth_page.setObjectName(u"min_max_teeth_page")
        self.min_max_teeth_page.setGeometry(QRect(0, 0, 431, 438))
        self.verticalLayoutWidget = QWidget(self.min_max_teeth_page)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 431, 111))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.min_sun_teeth_spinbox = QSpinBox(self.verticalLayoutWidget)
        self.min_sun_teeth_spinbox.setObjectName(u"min_sun_teeth_spinbox")
        self.min_sun_teeth_spinbox.setMinimum(3)
        self.min_sun_teeth_spinbox.setMaximum(99999)

        self.horizontalLayout.addWidget(self.min_sun_teeth_spinbox)

        self.min_sun_teeth_spinbox_lock = LockUnlockButton(self.verticalLayoutWidget)
        self.min_sun_teeth_spinbox_lock.setObjectName(u"min_sun_teeth_spinbox_lock")

        self.horizontalLayout.addWidget(self.min_sun_teeth_spinbox_lock)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.max_sun_teeth_spinbox = QSpinBox(self.verticalLayoutWidget)
        self.max_sun_teeth_spinbox.setObjectName(u"max_sun_teeth_spinbox")
        self.max_sun_teeth_spinbox.setMinimum(3)
        self.max_sun_teeth_spinbox.setMaximum(99999)

        self.horizontalLayout.addWidget(self.max_sun_teeth_spinbox)

        self.max_sun_teeth_spinbox_lock = LockUnlockButton(self.verticalLayoutWidget)
        self.max_sun_teeth_spinbox_lock.setObjectName(u"max_sun_teeth_spinbox_lock")

        self.horizontalLayout.addWidget(self.max_sun_teeth_spinbox_lock)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.min_planet_teeth_spinbox = QSpinBox(self.verticalLayoutWidget)
        self.min_planet_teeth_spinbox.setObjectName(u"min_planet_teeth_spinbox")
        self.min_planet_teeth_spinbox.setMinimum(3)
        self.min_planet_teeth_spinbox.setMaximum(99999)

        self.horizontalLayout_2.addWidget(self.min_planet_teeth_spinbox)

        self.min_planet_teeth_spinbox_lock = LockUnlockButton(self.verticalLayoutWidget)
        self.min_planet_teeth_spinbox_lock.setObjectName(u"min_planet_teeth_spinbox_lock")

        self.horizontalLayout_2.addWidget(self.min_planet_teeth_spinbox_lock)

        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.max_planet_teeth_spinbox = QSpinBox(self.verticalLayoutWidget)
        self.max_planet_teeth_spinbox.setObjectName(u"max_planet_teeth_spinbox")
        self.max_planet_teeth_spinbox.setMinimum(3)
        self.max_planet_teeth_spinbox.setMaximum(99999)

        self.horizontalLayout_2.addWidget(self.max_planet_teeth_spinbox)

        self.max_planet_teeth_spinbox_lock = LockUnlockButton(self.verticalLayoutWidget)
        self.max_planet_teeth_spinbox_lock.setObjectName(u"max_planet_teeth_spinbox_lock")

        self.horizontalLayout_2.addWidget(self.max_planet_teeth_spinbox_lock)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.min_ring_teeth_spinbox = QSpinBox(self.verticalLayoutWidget)
        self.min_ring_teeth_spinbox.setObjectName(u"min_ring_teeth_spinbox")
        self.min_ring_teeth_spinbox.setMinimum(3)
        self.min_ring_teeth_spinbox.setMaximum(99999)

        self.horizontalLayout_3.addWidget(self.min_ring_teeth_spinbox)

        self.min_ring_teeth_spinbox_lock = LockUnlockButton(self.verticalLayoutWidget)
        self.min_ring_teeth_spinbox_lock.setObjectName(u"min_ring_teeth_spinbox_lock")

        self.horizontalLayout_3.addWidget(self.min_ring_teeth_spinbox_lock)

        self.label_6 = QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.max_ring_teeth_spinbox = QSpinBox(self.verticalLayoutWidget)
        self.max_ring_teeth_spinbox.setObjectName(u"max_ring_teeth_spinbox")
        self.max_ring_teeth_spinbox.setMinimum(3)
        self.max_ring_teeth_spinbox.setMaximum(99999)

        self.horizontalLayout_3.addWidget(self.max_ring_teeth_spinbox)

        self.max_ring_teeth_spinbox_lock = LockUnlockButton(self.verticalLayoutWidget)
        self.max_ring_teeth_spinbox_lock.setObjectName(u"max_ring_teeth_spinbox_lock")

        self.horizontalLayout_3.addWidget(self.max_ring_teeth_spinbox_lock)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.toolBox.addItem(self.min_max_teeth_page, u"Min/Max Teeth")
        self.planetary_ratio_page = QWidget()
        self.planetary_ratio_page.setObjectName(u"planetary_ratio_page")
        self.planetary_ratio_page.setGeometry(QRect(0, 0, 431, 438))
        self.gridLayoutWidget = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 177, 89))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.output_combobox_lock = LockUnlockButton(self.gridLayoutWidget)
        self.output_combobox_lock.setObjectName(u"output_combobox_lock")

        self.gridLayout.addWidget(self.output_combobox_lock, 1, 2, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)

        self.input_combobox = QComboBox(self.gridLayoutWidget)
        self.input_combobox.addItem("")
        self.input_combobox.addItem("")
        self.input_combobox.addItem("")
        self.input_combobox.setObjectName(u"input_combobox")

        self.gridLayout.addWidget(self.input_combobox, 0, 1, 1, 1)

        self.label_14 = QLabel(self.gridLayoutWidget)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 1, 0, 1, 1)

        self.output_combobox = QComboBox(self.gridLayoutWidget)
        self.output_combobox.addItem("")
        self.output_combobox.addItem("")
        self.output_combobox.addItem("")
        self.output_combobox.setObjectName(u"output_combobox")

        self.gridLayout.addWidget(self.output_combobox, 1, 1, 1, 1)

        self.input_combobo_lock = LockUnlockButton(self.gridLayoutWidget)
        self.input_combobo_lock.setObjectName(u"input_combobo_lock")

        self.gridLayout.addWidget(self.input_combobo_lock, 0, 2, 1, 1)

        self.label_15 = QLabel(self.gridLayoutWidget)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 2, 0, 1, 1)

        self.fixed_combobox = QComboBox(self.gridLayoutWidget)
        self.fixed_combobox.addItem("")
        self.fixed_combobox.addItem("")
        self.fixed_combobox.addItem("")
        self.fixed_combobox.setObjectName(u"fixed_combobox")

        self.gridLayout.addWidget(self.fixed_combobox, 2, 1, 1, 1)

        self.fixed_combobox_lock = LockUnlockButton(self.gridLayoutWidget)
        self.fixed_combobox_lock.setObjectName(u"fixed_combobox_lock")

        self.gridLayout.addWidget(self.fixed_combobox_lock, 2, 2, 1, 1)

        self.gridLayoutWidget_2 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(0, 100, 208, 90))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_35 = QLabel(self.gridLayoutWidget_2)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_2.addWidget(self.label_35, 0, 0, 1, 1)

        self.gear_addendum_lineedit = QLineEdit(self.gridLayoutWidget_2)
        self.gear_addendum_lineedit.setObjectName(u"gear_addendum_lineedit")

        self.gridLayout_2.addWidget(self.gear_addendum_lineedit, 0, 1, 1, 1)

        self.planet_clearance_lineedit = QLineEdit(self.gridLayoutWidget_2)
        self.planet_clearance_lineedit.setObjectName(u"planet_clearance_lineedit")

        self.gridLayout_2.addWidget(self.planet_clearance_lineedit, 1, 1, 1, 1)

        self.gear_addendum_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_2)
        self.gear_addendum_lineedit_lock.setObjectName(u"gear_addendum_lineedit_lock")

        self.gridLayout_2.addWidget(self.gear_addendum_lineedit_lock, 0, 2, 1, 1)

        self.planet_clearance_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_2)
        self.planet_clearance_lineedit_lock.setObjectName(u"planet_clearance_lineedit_lock")

        self.gridLayout_2.addWidget(self.planet_clearance_lineedit_lock, 1, 2, 1, 1)

        self.label_34 = QLabel(self.gridLayoutWidget_2)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_2.addWidget(self.label_34, 1, 0, 1, 1)

        self.label_33 = QLabel(self.gridLayoutWidget_2)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_2.addWidget(self.label_33, 2, 0, 1, 1)

        self.number_of_planets_spinbox = QSpinBox(self.gridLayoutWidget_2)
        self.number_of_planets_spinbox.setObjectName(u"number_of_planets_spinbox")
        self.number_of_planets_spinbox.setMinimum(1)
        self.number_of_planets_spinbox.setMaximum(99999)

        self.gridLayout_2.addWidget(self.number_of_planets_spinbox, 2, 1, 1, 1)

        self.number_of_planets_spinbox_lock = LockUnlockButton(self.gridLayoutWidget_2)
        self.number_of_planets_spinbox_lock.setObjectName(u"number_of_planets_spinbox_lock")

        self.gridLayout_2.addWidget(self.number_of_planets_spinbox_lock, 2, 2, 1, 1)

        self.gridLayoutWidget_3 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(0, 200, 299, 89))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.target_gear_ratio_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_3)
        self.target_gear_ratio_lineedit_lock.setObjectName(u"target_gear_ratio_lineedit_lock")
        self.target_gear_ratio_lineedit_lock.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_3.addWidget(self.target_gear_ratio_lineedit_lock, 0, 2, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)

        self.gear_ratio_options_progress = QProgressBar(self.gridLayoutWidget_3)
        self.gear_ratio_options_progress.setObjectName(u"gear_ratio_options_progress")
        self.gear_ratio_options_progress.setValue(24)

        self.gridLayout_3.addWidget(self.gear_ratio_options_progress, 1, 1, 1, 1)

        self.target_cear_ratio_lineedit = QLineEdit(self.gridLayoutWidget_3)
        self.target_cear_ratio_lineedit.setObjectName(u"target_cear_ratio_lineedit")

        self.gridLayout_3.addWidget(self.target_cear_ratio_lineedit, 0, 1, 1, 1)

        self.gear_ratio_options_progress_abort = QPushButton(self.gridLayoutWidget_3)
        self.gear_ratio_options_progress_abort.setObjectName(u"gear_ratio_options_progress_abort")

        self.gridLayout_3.addWidget(self.gear_ratio_options_progress_abort, 1, 2, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 1)

        self.gear_ratio_options_combobox = QComboBox(self.gridLayoutWidget_3)
        self.gear_ratio_options_combobox.setObjectName(u"gear_ratio_options_combobox")

        self.gridLayout_3.addWidget(self.gear_ratio_options_combobox, 2, 1, 1, 1)

        self.gear_ratio_options_combobox_lock = LockUnlockButton(self.gridLayoutWidget_3)
        self.gear_ratio_options_combobox_lock.setObjectName(u"gear_ratio_options_combobox_lock")

        self.gridLayout_3.addWidget(self.gear_ratio_options_combobox_lock, 2, 2, 1, 1)

        self.gridLayoutWidget_4 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(0, 300, 291, 61))
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_36 = QLabel(self.gridLayoutWidget_4)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_4.addWidget(self.label_36, 0, 0, 1, 1)

        self.label_37 = QLabel(self.gridLayoutWidget_4)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_4.addWidget(self.label_37, 1, 0, 1, 1)

        self.is_planet_neighbor_constraint_satisfied_indicator_label = QLabel(self.gridLayoutWidget_4)
        self.is_planet_neighbor_constraint_satisfied_indicator_label.setObjectName(u"is_planet_neighbor_constraint_satisfied_indicator_label")

        self.gridLayout_4.addWidget(self.is_planet_neighbor_constraint_satisfied_indicator_label, 0, 1, 1, 1)

        self.is_homogeneity_distribution_constraint_satisfied_indicator_label = QLabel(self.gridLayoutWidget_4)
        self.is_homogeneity_distribution_constraint_satisfied_indicator_label.setObjectName(u"is_homogeneity_distribution_constraint_satisfied_indicator_label")

        self.gridLayout_4.addWidget(self.is_homogeneity_distribution_constraint_satisfied_indicator_label, 1, 1, 1, 1)

        self.toolBox.addItem(self.planetary_ratio_page, u"Planetary Ratio")
        self.shape_page = QWidget()
        self.shape_page.setObjectName(u"shape_page")
        self.shape_page.setGeometry(QRect(0, 0, 431, 438))
        self.gridLayoutWidget_5 = QWidget(self.shape_page)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(0, 0, 260, 89))
        self.gridLayout_5 = QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.gridLayoutWidget_5)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_5.addWidget(self.label_12, 1, 0, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget_5)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)

        self.yield_strength_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_5)
        self.yield_strength_lineedit_lock.setObjectName(u"yield_strength_lineedit_lock")

        self.gridLayout_5.addWidget(self.yield_strength_lineedit_lock, 1, 2, 1, 1)

        self.material_combobox = QComboBox(self.gridLayoutWidget_5)
        self.material_combobox.setObjectName(u"material_combobox")

        self.gridLayout_5.addWidget(self.material_combobox, 0, 1, 1, 1)

        self.material_combobox_lock = LockUnlockButton(self.gridLayoutWidget_5)
        self.material_combobox_lock.setObjectName(u"material_combobox_lock")

        self.gridLayout_5.addWidget(self.material_combobox_lock, 0, 2, 1, 1)

        self.yield_strength_lineedit = QLineEdit(self.gridLayoutWidget_5)
        self.yield_strength_lineedit.setObjectName(u"yield_strength_lineedit")

        self.gridLayout_5.addWidget(self.yield_strength_lineedit, 1, 1, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget_5)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_5.addWidget(self.label_13, 2, 0, 1, 1)

        self.sliding_friction_lineedit = QLineEdit(self.gridLayoutWidget_5)
        self.sliding_friction_lineedit.setObjectName(u"sliding_friction_lineedit")

        self.gridLayout_5.addWidget(self.sliding_friction_lineedit, 2, 1, 1, 1)

        self.sliding_friction_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_5)
        self.sliding_friction_lineedit_lock.setObjectName(u"sliding_friction_lineedit_lock")

        self.gridLayout_5.addWidget(self.sliding_friction_lineedit_lock, 2, 2, 1, 1)

        self.gridLayoutWidget_6 = QWidget(self.shape_page)
        self.gridLayoutWidget_6.setObjectName(u"gridLayoutWidget_6")
        self.gridLayoutWidget_6.setGeometry(QRect(0, 100, 264, 120))
        self.gridLayout_6 = QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.pressure_angle_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_6)
        self.pressure_angle_lineedit_lock.setObjectName(u"pressure_angle_lineedit_lock")

        self.gridLayout_6.addWidget(self.pressure_angle_lineedit_lock, 3, 2, 1, 1)

        self.module_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.module_lineedit.setObjectName(u"module_lineedit")
        self.module_lineedit.setEnabled(True)

        self.gridLayout_6.addWidget(self.module_lineedit, 0, 1, 1, 1)

        self.ring_pitch_circle_diam_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.ring_pitch_circle_diam_lineedit.setObjectName(u"ring_pitch_circle_diam_lineedit")
        self.ring_pitch_circle_diam_lineedit.setEnabled(True)

        self.gridLayout_6.addWidget(self.ring_pitch_circle_diam_lineedit, 1, 1, 1, 1)

        self.module_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_6)
        self.module_lineedit_lock.setObjectName(u"module_lineedit_lock")

        self.gridLayout_6.addWidget(self.module_lineedit_lock, 0, 2, 1, 1)

        self.ring_pitch_circle_diam_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_6)
        self.ring_pitch_circle_diam_lineedit_lock.setObjectName(u"ring_pitch_circle_diam_lineedit_lock")

        self.gridLayout_6.addWidget(self.ring_pitch_circle_diam_lineedit_lock, 1, 2, 1, 1)

        self.label_19 = QLabel(self.gridLayoutWidget_6)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 0, 0, 1, 1)

        self.label_21 = QLabel(self.gridLayoutWidget_6)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_6.addWidget(self.label_21, 3, 0, 1, 1)

        self.pressure_angle_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.pressure_angle_lineedit.setObjectName(u"pressure_angle_lineedit")
        self.pressure_angle_lineedit.setEnabled(True)

        self.gridLayout_6.addWidget(self.pressure_angle_lineedit, 3, 1, 1, 1)

        self.label_20 = QLabel(self.gridLayoutWidget_6)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_6.addWidget(self.label_20, 1, 0, 1, 1)

        self.label_24 = QLabel(self.gridLayoutWidget_6)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_6.addWidget(self.label_24, 2, 0, 1, 1)

        self.sun_pitch_circle_diam_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.sun_pitch_circle_diam_lineedit.setObjectName(u"sun_pitch_circle_diam_lineedit")
        self.sun_pitch_circle_diam_lineedit.setEnabled(True)

        self.gridLayout_6.addWidget(self.sun_pitch_circle_diam_lineedit, 2, 1, 1, 1)

        self.sun_pitch_circle_diam_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_6)
        self.sun_pitch_circle_diam_lineedit_lock.setObjectName(u"sun_pitch_circle_diam_lineedit_lock")

        self.gridLayout_6.addWidget(self.sun_pitch_circle_diam_lineedit_lock, 2, 2, 1, 1)

        self.gridLayoutWidget_7 = QWidget(self.shape_page)
        self.gridLayoutWidget_7.setObjectName(u"gridLayoutWidget_7")
        self.gridLayoutWidget_7.setGeometry(QRect(0, 230, 261, 89))
        self.gridLayout_7 = QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_16 = QLabel(self.gridLayoutWidget_7)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_7.addWidget(self.label_16, 0, 0, 1, 1)

        self.label_17 = QLabel(self.gridLayoutWidget_7)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_7.addWidget(self.label_17, 1, 0, 1, 1)

        self.efficiency_indicator_lineedit = QLineEdit(self.gridLayoutWidget_7)
        self.efficiency_indicator_lineedit.setObjectName(u"efficiency_indicator_lineedit")
        self.efficiency_indicator_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.efficiency_indicator_lineedit, 1, 1, 1, 1)

        self.label_18 = QLabel(self.gridLayoutWidget_7)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_7.addWidget(self.label_18, 2, 0, 1, 1)

        self.minimum_height_indicator_lineedit = QLineEdit(self.gridLayoutWidget_7)
        self.minimum_height_indicator_lineedit.setObjectName(u"minimum_height_indicator_lineedit")
        self.minimum_height_indicator_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.minimum_height_indicator_lineedit, 0, 1, 1, 1)

        self.height_lineedit = QLineEdit(self.gridLayoutWidget_7)
        self.height_lineedit.setObjectName(u"height_lineedit")
        self.height_lineedit.setEnabled(True)

        self.gridLayout_7.addWidget(self.height_lineedit, 2, 1, 1, 1)

        self.height_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_7)
        self.height_lineedit_lock.setObjectName(u"height_lineedit_lock")

        self.gridLayout_7.addWidget(self.height_lineedit_lock, 2, 2, 1, 1)

        self.gridLayoutWidget_8 = QWidget(self.shape_page)
        self.gridLayoutWidget_8.setObjectName(u"gridLayoutWidget_8")
        self.gridLayoutWidget_8.setGeometry(QRect(0, 330, 261, 61))
        self.gridLayout_8 = QGridLayout(self.gridLayoutWidget_8)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.beta_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_8)
        self.beta_lineedit_lock.setObjectName(u"beta_lineedit_lock")

        self.gridLayout_8.addWidget(self.beta_lineedit_lock, 0, 2, 1, 1)

        self.beta_lineedit = QLineEdit(self.gridLayoutWidget_8)
        self.beta_lineedit.setObjectName(u"beta_lineedit")
        self.beta_lineedit.setEnabled(True)

        self.gridLayout_8.addWidget(self.beta_lineedit, 0, 1, 1, 1)

        self.label_22 = QLabel(self.gridLayoutWidget_8)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_8.addWidget(self.label_22, 0, 0, 1, 1)

        self.label_23 = QLabel(self.gridLayoutWidget_8)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_8.addWidget(self.label_23, 1, 0, 1, 1)

        self.double_helix_checkbox = QCheckBox(self.gridLayoutWidget_8)
        self.double_helix_checkbox.setObjectName(u"double_helix_checkbox")

        self.gridLayout_8.addWidget(self.double_helix_checkbox, 1, 1, 1, 1)

        self.double_helix_checkbox_lock = LockUnlockButton(self.gridLayoutWidget_8)
        self.double_helix_checkbox_lock.setObjectName(u"double_helix_checkbox_lock")

        self.gridLayout_8.addWidget(self.double_helix_checkbox_lock, 1, 2, 1, 1)

        self.toolBox.addItem(self.shape_page, u"Shape")

        self.retranslateUi(Dialog)

        self.toolBox.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Min Sun Teeth:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Max Sun Teeth:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Min Planet Teeth:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Max Planet Teeth:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Min Ring Teeth:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Max Ring Teeth:", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.min_max_teeth_page), QCoreApplication.translate("Dialog", u"Min/Max Teeth", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Input:", None))
        self.input_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"Sun", None))
        self.input_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Ring", None))
        self.input_combobox.setItemText(2, QCoreApplication.translate("Dialog", u"Carrier", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"Output:", None))
        self.output_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"Carrier", None))
        self.output_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Sun", None))
        self.output_combobox.setItemText(2, QCoreApplication.translate("Dialog", u"Ring", None))

        self.label_15.setText(QCoreApplication.translate("Dialog", u"Fixed:", None))
        self.fixed_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"Ring", None))
        self.fixed_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Sun", None))
        self.fixed_combobox.setItemText(2, QCoreApplication.translate("Dialog", u"Carrier", None))

        self.label_35.setText(QCoreApplication.translate("Dialog", u"Gear Addendum:", None))
        self.label_34.setText(QCoreApplication.translate("Dialog", u"Planet Clearance:", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"Number of Planets:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Target Gear Ratio:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Calculating Options:", None))
        self.gear_ratio_options_progress_abort.setText(QCoreApplication.translate("Dialog", u"Abort", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Options:", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Is planet neighbor constraint satisfied:", None))
        self.label_37.setText(QCoreApplication.translate("Dialog", u"Is homogeneity distribution constraint satisfied:", None))
        self.is_planet_neighbor_constraint_satisfied_indicator_label.setText(QCoreApplication.translate("Dialog", u"X", None))
        self.is_homogeneity_distribution_constraint_satisfied_indicator_label.setText(QCoreApplication.translate("Dialog", u"X", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.planetary_ratio_page), QCoreApplication.translate("Dialog", u"Planetary Ratio", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Yield Strength:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Material:", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Sliding Friction Coefficient:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Module:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Pressure Angle:", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Ring Pitch Circle Diameter:", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"Sun Pitch Circle Diameter:", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Minimum Height:", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Efficiency:", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Height:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Beta:", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Double Helix:", None))
        self.double_helix_checkbox.setText("")
        self.toolBox.setItemText(self.toolBox.indexOf(self.shape_page), QCoreApplication.translate("Dialog", u"Shape", None))
    # retranslateUi

