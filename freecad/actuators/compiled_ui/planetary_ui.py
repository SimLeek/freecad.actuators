# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gear-selectorsRuOJTd.ui'
##
## Created by: Qt User Interface Compiler version 5.15.16
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from .lock_button_ui import LockUnlockButton
from .length_ui import QLengthEdit
from .fraction_ui import QFractionEdit
from .torque_ui import QTorqueEdit
from .pressure_ui import QPressureEdit
from .eval_ui import QEvalEdit
from .angle_ui import QAngleEdit


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(448, 550)
        self.toolBox = QToolBox(Dialog)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setGeometry(QRect(10, 20, 431, 511))
        self.min_max_teeth_page = QWidget()
        self.min_max_teeth_page.setObjectName(u"min_max_teeth_page")
        self.min_max_teeth_page.setGeometry(QRect(0, 0, 431, 387))
        self.verticalLayoutWidget = QWidget(self.min_max_teeth_page)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 100, 431, 111))
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

        self.gridLayoutWidget = QWidget(self.min_max_teeth_page)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 210, 177, 89))
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
        self.fixed_combobox.addItem("")
        self.fixed_combobox.setObjectName(u"fixed_combobox")

        self.gridLayout.addWidget(self.fixed_combobox, 2, 1, 1, 1)

        self.fixed_combobox_lock = LockUnlockButton(self.gridLayoutWidget)
        self.fixed_combobox_lock.setObjectName(u"fixed_combobox_lock")

        self.gridLayout.addWidget(self.fixed_combobox_lock, 2, 2, 1, 1)

        self.gridLayoutWidget_14 = QWidget(self.min_max_teeth_page)
        self.gridLayoutWidget_14.setObjectName(u"gridLayoutWidget_14")
        self.gridLayoutWidget_14.setGeometry(QRect(0, 300, 251, 58))
        self.gridLayout_14 = QGridLayout(self.gridLayoutWidget_14)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.min_height_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_14)
        self.min_height_lineedit_lock.setObjectName(u"min_height_lineedit_lock")

        self.gridLayout_14.addWidget(self.min_height_lineedit_lock, 0, 2, 1, 1)

        self.min_height_lineedit = QLengthEdit(self.gridLayoutWidget_14)
        self.min_height_lineedit.setObjectName(u"min_height_lineedit")
        self.min_height_lineedit.setEnabled(True)

        self.gridLayout_14.addWidget(self.min_height_lineedit, 0, 1, 1, 1)

        self.label_46 = QLabel(self.gridLayoutWidget_14)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_14.addWidget(self.label_46, 0, 0, 1, 1)

        self.label_47 = QLabel(self.gridLayoutWidget_14)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_14.addWidget(self.label_47, 1, 0, 1, 1)

        self.max_height_lineedit = QLengthEdit(self.gridLayoutWidget_14)
        self.max_height_lineedit.setObjectName(u"max_height_lineedit")
        self.max_height_lineedit.setEnabled(True)

        self.gridLayout_14.addWidget(self.max_height_lineedit, 1, 1, 1, 1)

        self.max_height_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_14)
        self.max_height_lineedit_lock.setObjectName(u"max_height_lineedit_lock")

        self.gridLayout_14.addWidget(self.max_height_lineedit_lock, 1, 2, 1, 1)

        self.gridLayoutWidget_12 = QWidget(self.min_max_teeth_page)
        self.gridLayoutWidget_12.setObjectName(u"gridLayoutWidget_12")
        self.gridLayoutWidget_12.setGeometry(QRect(0, 40, 251, 58))
        self.gridLayout_12 = QGridLayout(self.gridLayoutWidget_12)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_40 = QLabel(self.gridLayoutWidget_12)
        self.label_40.setObjectName(u"label_40")

        self.gridLayout_12.addWidget(self.label_40, 0, 0, 1, 1)

        self.min_module_lineedit = QLengthEdit(self.gridLayoutWidget_12)
        self.min_module_lineedit.setObjectName(u"min_module_lineedit")
        self.min_module_lineedit.setEnabled(True)

        self.gridLayout_12.addWidget(self.min_module_lineedit, 0, 1, 1, 1)

        self.min_module_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_12)
        self.min_module_lineedit_lock.setObjectName(u"min_module_lineedit_lock")

        self.gridLayout_12.addWidget(self.min_module_lineedit_lock, 0, 2, 1, 1)

        self.label_41 = QLabel(self.gridLayoutWidget_12)
        self.label_41.setObjectName(u"label_41")

        self.gridLayout_12.addWidget(self.label_41, 1, 0, 1, 1)

        self.min_circular_pitch_lineedit = QLengthEdit(self.gridLayoutWidget_12)
        self.min_circular_pitch_lineedit.setObjectName(u"min_circular_pitch_lineedit")
        self.min_circular_pitch_lineedit.setEnabled(True)

        self.gridLayout_12.addWidget(self.min_circular_pitch_lineedit, 1, 1, 1, 1)

        self.label_42 = QLabel(self.gridLayoutWidget_12)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setAlignment(Qt.AlignCenter)

        self.gridLayout_12.addWidget(self.label_42, 1, 2, 1, 1)

        self.gridLayoutWidget_15 = QWidget(self.min_max_teeth_page)
        self.gridLayoutWidget_15.setObjectName(u"gridLayoutWidget_15")
        self.gridLayoutWidget_15.setGeometry(QRect(0, 10, 251, 31))
        self.gridLayout_15 = QGridLayout(self.gridLayoutWidget_15)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.label_48 = QLabel(self.gridLayoutWidget_15)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_15.addWidget(self.label_48, 0, 0, 1, 1)

        self.max_ring_diam_lineedit = QLengthEdit(self.gridLayoutWidget_15)
        self.max_ring_diam_lineedit.setObjectName(u"max_ring_diam_lineedit")
        self.max_ring_diam_lineedit.setEnabled(True)

        self.gridLayout_15.addWidget(self.max_ring_diam_lineedit, 0, 1, 1, 1)

        self.max_ring_diam_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_15)
        self.max_ring_diam_lineedit_lock.setObjectName(u"max_ring_diam_lineedit_lock")

        self.gridLayout_15.addWidget(self.max_ring_diam_lineedit_lock, 0, 2, 1, 1)

        self.toolBox.addItem(self.min_max_teeth_page, u"Constraints")
        self.planetary_ratio_page = QWidget()
        self.planetary_ratio_page.setObjectName(u"planetary_ratio_page")
        self.planetary_ratio_page.setGeometry(QRect(0, 0, 431, 387))
        self.gridLayoutWidget_3 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 140, 385, 89))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.gridLayoutWidget_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)

        self.gear_ratio_options_abort = QPushButton(self.gridLayoutWidget_3)
        self.gear_ratio_options_abort.setObjectName(u"gear_ratio_options_abort")

        self.gridLayout_3.addWidget(self.gear_ratio_options_abort, 2, 3, 1, 1)

        self.gear_ratio_options_progress = QProgressBar(self.gridLayoutWidget_3)
        self.gear_ratio_options_progress.setObjectName(u"gear_ratio_options_progress")
        self.gear_ratio_options_progress.setValue(100)

        self.gridLayout_3.addWidget(self.gear_ratio_options_progress, 2, 1, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 3, 0, 1, 1)

        self.gear_ratio_options_combobox = QComboBox(self.gridLayoutWidget_3)
        self.gear_ratio_options_combobox.setObjectName(u"gear_ratio_options_combobox")

        self.gridLayout_3.addWidget(self.gear_ratio_options_combobox, 3, 1, 1, 1)

        self.target_cear_ratio_lineedit = QFractionEdit(self.gridLayoutWidget_3)
        self.target_cear_ratio_lineedit.setObjectName(u"target_cear_ratio_lineedit")

        self.gridLayout_3.addWidget(self.target_cear_ratio_lineedit, 0, 1, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.gear_ratio_options_calculate = QPushButton(self.gridLayoutWidget_3)
        self.gear_ratio_options_calculate.setObjectName(u"gear_ratio_options_calculate")

        self.gridLayout_3.addWidget(self.gear_ratio_options_calculate, 2, 2, 1, 1)

        self.target_gear_ratio_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_3)
        self.target_gear_ratio_lineedit_lock.setObjectName(u"target_gear_ratio_lineedit_lock")
        self.target_gear_ratio_lineedit_lock.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_3.addWidget(self.target_gear_ratio_lineedit_lock, 0, 2, 1, 1)

        self.gear_ratio_options_combobox_lock = LockUnlockButton(self.gridLayoutWidget_3)
        self.gear_ratio_options_combobox_lock.setObjectName(u"gear_ratio_options_combobox_lock")

        self.gridLayout_3.addWidget(self.gear_ratio_options_combobox_lock, 3, 2, 1, 1)

        self.gridLayoutWidget_4 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 320, 301, 61))
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

        self.gridLayoutWidget_2 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 0, 231, 141))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.planet_clearance_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_2)
        self.planet_clearance_lineedit_lock.setObjectName(u"planet_clearance_lineedit_lock")

        self.gridLayout_2.addWidget(self.planet_clearance_lineedit_lock, 1, 2, 1, 1)

        self.label_34 = QLabel(self.gridLayoutWidget_2)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_2.addWidget(self.label_34, 1, 0, 1, 1)

        self.gear_addendum_lineedit = QLengthEdit(self.gridLayoutWidget_2)
        self.gear_addendum_lineedit.setObjectName(u"gear_addendum_lineedit")

        self.gridLayout_2.addWidget(self.gear_addendum_lineedit, 0, 1, 1, 1)

        self.num_results_spinbox = QSpinBox(self.gridLayoutWidget_2)
        self.num_results_spinbox.setObjectName(u"num_results_spinbox")
        self.num_results_spinbox.setMinimum(1)
        self.num_results_spinbox.setMaximum(99999)

        self.gridLayout_2.addWidget(self.num_results_spinbox, 3, 1, 1, 1)

        self.num_results_spinbox_lock = LockUnlockButton(self.gridLayoutWidget_2)
        self.num_results_spinbox_lock.setObjectName(u"num_results_spinbox_lock")

        self.gridLayout_2.addWidget(self.num_results_spinbox_lock, 3, 2, 1, 1)

        self.gear_addendum_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_2)
        self.gear_addendum_lineedit_lock.setObjectName(u"gear_addendum_lineedit_lock")

        self.gridLayout_2.addWidget(self.gear_addendum_lineedit_lock, 0, 2, 1, 1)

        self.number_of_planets_spinbox_lock = LockUnlockButton(self.gridLayoutWidget_2)
        self.number_of_planets_spinbox_lock.setObjectName(u"number_of_planets_spinbox_lock")

        self.gridLayout_2.addWidget(self.number_of_planets_spinbox_lock, 2, 2, 1, 1)

        self.label_33 = QLabel(self.gridLayoutWidget_2)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_2.addWidget(self.label_33, 2, 0, 1, 1)

        self.number_of_planets_spinbox = QSpinBox(self.gridLayoutWidget_2)
        self.number_of_planets_spinbox.setObjectName(u"number_of_planets_spinbox")
        self.number_of_planets_spinbox.setMinimum(3)
        self.number_of_planets_spinbox.setMaximum(99999)

        self.gridLayout_2.addWidget(self.number_of_planets_spinbox, 2, 1, 1, 1)

        self.label_35 = QLabel(self.gridLayoutWidget_2)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_2.addWidget(self.label_35, 0, 0, 1, 1)

        self.planet_clearance_lineedit = QLengthEdit(self.gridLayoutWidget_2)
        self.planet_clearance_lineedit.setObjectName(u"planet_clearance_lineedit")

        self.gridLayout_2.addWidget(self.planet_clearance_lineedit, 1, 1, 1, 1)

        self.label_43 = QLabel(self.gridLayoutWidget_2)
        self.label_43.setObjectName(u"label_43")

        self.gridLayout_2.addWidget(self.label_43, 3, 0, 1, 1)

        self.label_44 = QLabel(self.gridLayoutWidget_2)
        self.label_44.setObjectName(u"label_44")

        self.gridLayout_2.addWidget(self.label_44, 4, 0, 1, 1)

        self.use_abs_checkbox = QCheckBox(self.gridLayoutWidget_2)
        self.use_abs_checkbox.setObjectName(u"use_abs_checkbox")

        self.gridLayout_2.addWidget(self.use_abs_checkbox, 4, 1, 1, 1)

        self.gridLayoutWidget_11 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_11.setObjectName(u"gridLayoutWidget_11")
        self.gridLayoutWidget_11.setGeometry(QRect(10, 230, 301, 89))
        self.gridLayout_11 = QGridLayout(self.gridLayoutWidget_11)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_20 = QLabel(self.gridLayoutWidget_11)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_11.addWidget(self.label_20, 0, 0, 1, 1)

        self.ring_pitch_circle_diam_lineedit = QLengthEdit(self.gridLayoutWidget_11)
        self.ring_pitch_circle_diam_lineedit.setObjectName(u"ring_pitch_circle_diam_lineedit")
        self.ring_pitch_circle_diam_lineedit.setEnabled(True)

        self.gridLayout_11.addWidget(self.ring_pitch_circle_diam_lineedit, 0, 1, 1, 1)

        self.label_27 = QLabel(self.gridLayoutWidget_11)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_27, 0, 2, 1, 1)

        self.label_24 = QLabel(self.gridLayoutWidget_11)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_11.addWidget(self.label_24, 1, 0, 1, 1)

        self.label_28 = QLabel(self.gridLayoutWidget_11)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_28, 1, 2, 1, 1)

        self.sun_pitch_circle_diam_lineedit = QLengthEdit(self.gridLayoutWidget_11)
        self.sun_pitch_circle_diam_lineedit.setObjectName(u"sun_pitch_circle_diam_lineedit")
        self.sun_pitch_circle_diam_lineedit.setEnabled(True)

        self.gridLayout_11.addWidget(self.sun_pitch_circle_diam_lineedit, 1, 1, 1, 1)

        self.label_29 = QLabel(self.gridLayoutWidget_11)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_11.addWidget(self.label_29, 2, 0, 1, 1)

        self.sun_pitch_circle_diam_lineedit_2 = QLengthEdit(self.gridLayoutWidget_11)
        self.sun_pitch_circle_diam_lineedit_2.setObjectName(u"sun_pitch_circle_diam_lineedit_2")
        self.sun_pitch_circle_diam_lineedit_2.setEnabled(True)

        self.gridLayout_11.addWidget(self.sun_pitch_circle_diam_lineedit_2, 2, 1, 1, 1)

        self.label_30 = QLabel(self.gridLayoutWidget_11)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_30, 2, 2, 1, 1)

        self.toolBox.addItem(self.planetary_ratio_page, u"Planetary Ratio Calculator")
        self.shape_page = QWidget()
        self.shape_page.setObjectName(u"shape_page")
        self.shape_page.setGeometry(QRect(0, 0, 431, 387))
        self.gridLayoutWidget_5 = QWidget(self.shape_page)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(0, 90, 260, 89))
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

        self.yield_strength_lineedit = QPressureEdit(self.gridLayoutWidget_5)
        self.yield_strength_lineedit.setObjectName(u"yield_strength_lineedit")

        self.gridLayout_5.addWidget(self.yield_strength_lineedit, 1, 1, 1, 1)

        self.label_13 = QLabel(self.gridLayoutWidget_5)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_5.addWidget(self.label_13, 2, 0, 1, 1)

        self.sliding_friction_lineedit = QEvalEdit(self.gridLayoutWidget_5)
        self.sliding_friction_lineedit.setObjectName(u"sliding_friction_lineedit")

        self.gridLayout_5.addWidget(self.sliding_friction_lineedit, 2, 1, 1, 1)

        self.sliding_friction_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_5)
        self.sliding_friction_lineedit_lock.setObjectName(u"sliding_friction_lineedit_lock")

        self.gridLayout_5.addWidget(self.sliding_friction_lineedit_lock, 2, 2, 1, 1)

        self.gridLayoutWidget_9 = QWidget(self.shape_page)
        self.gridLayoutWidget_9.setObjectName(u"gridLayoutWidget_9")
        self.gridLayoutWidget_9.setGeometry(QRect(0, 340, 261, 31))
        self.gridLayout_9 = QGridLayout(self.gridLayoutWidget_9)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_21 = QLabel(self.gridLayoutWidget_9)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_9.addWidget(self.label_21, 0, 0, 1, 1)

        self.pressure_angle_lineedit = QAngleEdit(self.gridLayoutWidget_9)
        self.pressure_angle_lineedit.setObjectName(u"pressure_angle_lineedit")
        self.pressure_angle_lineedit.setEnabled(True)

        self.gridLayout_9.addWidget(self.pressure_angle_lineedit, 0, 1, 1, 1)

        self.pressure_angle_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_9)
        self.pressure_angle_lineedit_lock.setObjectName(u"pressure_angle_lineedit_lock")

        self.gridLayout_9.addWidget(self.pressure_angle_lineedit_lock, 0, 2, 1, 1)

        self.gridLayoutWidget_6 = QWidget(self.shape_page)
        self.gridLayoutWidget_6.setObjectName(u"gridLayoutWidget_6")
        self.gridLayoutWidget_6.setGeometry(QRect(0, 180, 221, 89))
        self.gridLayout_6 = QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_26 = QLabel(self.gridLayoutWidget_6)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_26, 1, 2, 1, 1)

        self.module_lineedit = QLengthEdit(self.gridLayoutWidget_6)
        self.module_lineedit.setObjectName(u"module_lineedit")
        self.module_lineedit.setEnabled(True)

        self.gridLayout_6.addWidget(self.module_lineedit, 0, 1, 1, 1)

        self.module_lineedit_2 = QLengthEdit(self.gridLayoutWidget_6)
        self.module_lineedit_2.setObjectName(u"module_lineedit_2")
        self.module_lineedit_2.setEnabled(True)

        self.gridLayout_6.addWidget(self.module_lineedit_2, 1, 1, 1, 1)

        self.module_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_6)
        self.module_lineedit_lock.setObjectName(u"module_lineedit_lock")

        self.gridLayout_6.addWidget(self.module_lineedit_lock, 0, 2, 1, 1)

        self.label_25 = QLabel(self.gridLayoutWidget_6)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_6.addWidget(self.label_25, 1, 0, 1, 1)

        self.label_19 = QLabel(self.gridLayoutWidget_6)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 0, 0, 1, 1)

        self.label_18 = QLabel(self.gridLayoutWidget_6)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_6.addWidget(self.label_18, 2, 0, 1, 1)

        self.height_lineedit = QLengthEdit(self.gridLayoutWidget_6)
        self.height_lineedit.setObjectName(u"height_lineedit")
        self.height_lineedit.setEnabled(True)

        self.gridLayout_6.addWidget(self.height_lineedit, 2, 1, 1, 1)

        self.height_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_6)
        self.height_lineedit_lock.setObjectName(u"height_lineedit_lock")

        self.gridLayout_6.addWidget(self.height_lineedit_lock, 2, 2, 1, 1)

        self.gridLayoutWidget_8 = QWidget(self.shape_page)
        self.gridLayoutWidget_8.setObjectName(u"gridLayoutWidget_8")
        self.gridLayoutWidget_8.setGeometry(QRect(0, 270, 261, 61))
        self.gridLayout_8 = QGridLayout(self.gridLayoutWidget_8)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.beta_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_8)
        self.beta_lineedit_lock.setObjectName(u"beta_lineedit_lock")

        self.gridLayout_8.addWidget(self.beta_lineedit_lock, 0, 2, 1, 1)

        self.beta_lineedit = QAngleEdit(self.gridLayoutWidget_8)
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

        self.gridLayoutWidget_10 = QWidget(self.shape_page)
        self.gridLayoutWidget_10.setObjectName(u"gridLayoutWidget_10")
        self.gridLayoutWidget_10.setGeometry(QRect(0, 0, 261, 89))
        self.gridLayout_10 = QGridLayout(self.gridLayoutWidget_10)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_31 = QLabel(self.gridLayoutWidget_10)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_10.addWidget(self.label_31, 1, 0, 1, 1)

        self.label_17 = QLabel(self.gridLayoutWidget_10)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_10.addWidget(self.label_17, 0, 0, 1, 1)

        self.module_lineedit_3 = QTorqueEdit(self.gridLayoutWidget_10)
        self.module_lineedit_3.setObjectName(u"module_lineedit_3")
        self.module_lineedit_3.setEnabled(True)

        self.gridLayout_10.addWidget(self.module_lineedit_3, 0, 1, 1, 1)

        self.material_combobox_lock_2 = LockUnlockButton(self.gridLayoutWidget_10)
        self.material_combobox_lock_2.setObjectName(u"material_combobox_lock_2")

        self.gridLayout_10.addWidget(self.material_combobox_lock_2, 0, 2, 1, 1)

        self.label_32 = QLabel(self.gridLayoutWidget_10)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.label_32, 1, 2, 1, 1)

        self.module_lineedit_4 = QTorqueEdit(self.gridLayoutWidget_10)
        self.module_lineedit_4.setObjectName(u"module_lineedit_4")
        self.module_lineedit_4.setEnabled(True)

        self.gridLayout_10.addWidget(self.module_lineedit_4, 1, 1, 1, 1)

        self.label_38 = QLabel(self.gridLayoutWidget_10)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_10.addWidget(self.label_38, 2, 0, 1, 1)

        self.module_lineedit_5 = QTorqueEdit(self.gridLayoutWidget_10)
        self.module_lineedit_5.setObjectName(u"module_lineedit_5")
        self.module_lineedit_5.setEnabled(True)

        self.gridLayout_10.addWidget(self.module_lineedit_5, 2, 1, 1, 1)

        self.label_39 = QLabel(self.gridLayoutWidget_10)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.label_39, 2, 2, 1, 1)

        self.toolBox.addItem(self.shape_page, u"Material and Height Requirements")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.toolBox.addItem(self.page, u"Extras")

        self.retranslateUi(Dialog)

        self.toolBox.setCurrentIndex(0)
        self.output_combobox.setCurrentIndex(0)
        self.fixed_combobox.setCurrentIndex(0)


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
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Input:", None))
        self.input_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"Any", None))
        self.input_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Sun", None))
        self.input_combobox.setItemText(2, QCoreApplication.translate("Dialog", u"Ring", None))
        self.input_combobox.setItemText(3, QCoreApplication.translate("Dialog", u"Carrier", None))

        self.label_14.setText(QCoreApplication.translate("Dialog", u"Output:", None))
        self.output_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"Any", None))
        self.output_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Sun", None))
        self.output_combobox.setItemText(2, QCoreApplication.translate("Dialog", u"Ring", None))
        self.output_combobox.setItemText(3, QCoreApplication.translate("Dialog", u"Carrier", None))

        self.label_15.setText(QCoreApplication.translate("Dialog", u"Fixed:", None))
        self.fixed_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"Any", None))
        self.fixed_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Sun", None))
        self.fixed_combobox.setItemText(2, QCoreApplication.translate("Dialog", u"Ring", None))
        self.fixed_combobox.setItemText(3, QCoreApplication.translate("Dialog", u"Carrier", None))

        self.label_46.setText(QCoreApplication.translate("Dialog", u"Min height:", None))
        self.label_47.setText(QCoreApplication.translate("Dialog", u"Max height:", None))
        self.label_40.setText(QCoreApplication.translate("Dialog", u"Min Module:", None))
        self.label_41.setText(QCoreApplication.translate("Dialog", u"Min Circular Pitch:", None))
#if QT_CONFIG(tooltip)
        self.label_42.setToolTip(QCoreApplication.translate("Dialog", u"This entry sets or is set by sun torque", None))
#endif // QT_CONFIG(tooltip)
        self.label_42.setText(QCoreApplication.translate("Dialog", u"  =  ", None))
#if QT_CONFIG(tooltip)
        self.label_48.setToolTip(QCoreApplication.translate("Dialog", u"This assumes the ring is the full gear radius plus 2*addendum, usually 2*module.", None))
#endif // QT_CONFIG(tooltip)
        self.label_48.setText(QCoreApplication.translate("Dialog", u"Max Ring Diameter:", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.min_max_teeth_page), QCoreApplication.translate("Dialog", u"Constraints", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Calculating Options:", None))
        self.gear_ratio_options_abort.setText(QCoreApplication.translate("Dialog", u"Abort", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Options:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Target Gear Ratio:", None))
        self.gear_ratio_options_calculate.setText(QCoreApplication.translate("Dialog", u"Calculate", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Is planet neighbor constraint satisfied:", None))
        self.label_37.setText(QCoreApplication.translate("Dialog", u"Is homogeneity distribution constraint satisfied:", None))
        self.is_planet_neighbor_constraint_satisfied_indicator_label.setText(QCoreApplication.translate("Dialog", u"X", None))
        self.is_homogeneity_distribution_constraint_satisfied_indicator_label.setText(QCoreApplication.translate("Dialog", u"X", None))
        self.label_34.setText(QCoreApplication.translate("Dialog", u"Planet Clearance:", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"Number of Planets:", None))
        self.label_35.setText(QCoreApplication.translate("Dialog", u"Gear Addendum:", None))
        self.label_43.setText(QCoreApplication.translate("Dialog", u"Number of Options:", None))
        self.label_44.setText(QCoreApplication.translate("Dialog", u"Use Absolute Value:", None))
        self.use_abs_checkbox.setText("")
#if QT_CONFIG(tooltip)
        self.label_20.setToolTip(QCoreApplication.translate("Dialog", u"If you don't know module and want to define this, set the module to the smallest possible module such as 3d printer resolution*6, then define this once you have teeth counts", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Ring Pitch Circle Diameter:", None))
#if QT_CONFIG(tooltip)
        self.label_27.setToolTip(QCoreApplication.translate("Dialog", u"This entry sets or is set by module", None))
#endif // QT_CONFIG(tooltip)
        self.label_27.setText(QCoreApplication.translate("Dialog", u"=", None))
#if QT_CONFIG(tooltip)
        self.label_24.setToolTip(QCoreApplication.translate("Dialog", u"If you don't know module and want to define this, set the module to the smallest possible module such as 3d printer resolution*6, then define this once you have teeth counts", None))
#endif // QT_CONFIG(tooltip)
        self.label_24.setText(QCoreApplication.translate("Dialog", u"Sun Pitch Circle Diameter:", None))
#if QT_CONFIG(tooltip)
        self.label_28.setToolTip(QCoreApplication.translate("Dialog", u"This entry sets or is set by module", None))
#endif // QT_CONFIG(tooltip)
        self.label_28.setText(QCoreApplication.translate("Dialog", u"  =  ", None))
#if QT_CONFIG(tooltip)
        self.label_29.setToolTip(QCoreApplication.translate("Dialog", u"If you don't know module and want to define this, set the module to the smallest possible module such as 3d printer resolution*6, then define this once you have teeth counts", None))
#endif // QT_CONFIG(tooltip)
        self.label_29.setText(QCoreApplication.translate("Dialog", u"Planet Pitch Circle Diameter:", None))
#if QT_CONFIG(tooltip)
        self.label_30.setToolTip(QCoreApplication.translate("Dialog", u"This entry sets or is set by module", None))
#endif // QT_CONFIG(tooltip)
        self.label_30.setText(QCoreApplication.translate("Dialog", u"=", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.planetary_ratio_page), QCoreApplication.translate("Dialog", u"Planetary Ratio Calculator", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Yield Strength:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Material:", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Sliding Friction Coefficient:", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Pressure Angle:", None))
#if QT_CONFIG(tooltip)
        self.label_26.setToolTip(QCoreApplication.translate("Dialog", u"This entry sets or is set by module", None))
#endif // QT_CONFIG(tooltip)
        self.label_26.setText(QCoreApplication.translate("Dialog", u"=", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"Circular Pitch:", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Module:", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Height:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Beta:", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Double Helix:", None))
        self.double_helix_checkbox.setText("")
        self.label_31.setText(QCoreApplication.translate("Dialog", u"Ring Torque:", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Sun Torque:", None))
#if QT_CONFIG(tooltip)
        self.label_32.setToolTip(QCoreApplication.translate("Dialog", u"This entry sets or is set by sun torque", None))
#endif // QT_CONFIG(tooltip)
        self.label_32.setText(QCoreApplication.translate("Dialog", u"  =  ", None))
        self.label_38.setText(QCoreApplication.translate("Dialog", u"Carrier Torque:", None))
#if QT_CONFIG(tooltip)
        self.label_39.setToolTip(QCoreApplication.translate("Dialog", u"This entry sets or is set by sun torque", None))
#endif // QT_CONFIG(tooltip)
        self.label_39.setText(QCoreApplication.translate("Dialog", u"  =  ", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.shape_page), QCoreApplication.translate("Dialog", u"Material and Height Requirements", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QCoreApplication.translate("Dialog", u"Extras", None))
    # retranslateUi

