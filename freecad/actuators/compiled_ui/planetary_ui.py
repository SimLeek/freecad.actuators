# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gear-selectorsCGFYMC.ui'
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
from .angle_ui import QAngleEdit


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(484, 622)
        self.toolBox = QToolBox(Dialog)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setGeometry(QRect(10, 20, 461, 581))
        self.min_max_teeth_page = QWidget()
        self.min_max_teeth_page.setObjectName(u"min_max_teeth_page")
        self.min_max_teeth_page.setGeometry(QRect(0, 0, 461, 457))
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
        self.planetary_ratio_page.setGeometry(QRect(0, 0, 461, 457))
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
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayoutWidget_7 = QWidget(self.page_2)
        self.gridLayoutWidget_7.setObjectName(u"gridLayoutWidget_7")
        self.gridLayoutWidget_7.setGeometry(QRect(0, 120, 421, 151))
        self.gridLayout_7 = QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit, 1, 1, 1, 1)

        self.lineEdit_4 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_4, 3, 1, 1, 1)

        self.label_54 = QLabel(self.gridLayoutWidget_7)
        self.label_54.setObjectName(u"label_54")

        self.gridLayout_7.addWidget(self.label_54, 1, 4, 1, 1)

        self.lineEdit_11 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_11, 1, 7, 1, 1)

        self.label_61 = QLabel(self.gridLayoutWidget_7)
        self.label_61.setObjectName(u"label_61")

        self.gridLayout_7.addWidget(self.label_61, 4, 2, 1, 1)

        self.label_57 = QLabel(self.gridLayoutWidget_7)
        self.label_57.setObjectName(u"label_57")

        self.gridLayout_7.addWidget(self.label_57, 1, 6, 1, 1)

        self.label_52 = QLabel(self.gridLayoutWidget_7)
        self.label_52.setObjectName(u"label_52")

        self.gridLayout_7.addWidget(self.label_52, 2, 2, 1, 1)

        self.label_59 = QLabel(self.gridLayoutWidget_7)
        self.label_59.setObjectName(u"label_59")

        self.gridLayout_7.addWidget(self.label_59, 3, 6, 1, 1)

        self.label_53 = QLabel(self.gridLayoutWidget_7)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_7.addWidget(self.label_53, 3, 2, 1, 1)

        self.label_64 = QLabel(self.gridLayoutWidget_7)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_64, 3, 7, 1, 1)

        self.lineEdit_8 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_8, 1, 5, 1, 1)

        self.lineEdit_16 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_16, 4, 5, 1, 1)

        self.label_56 = QLabel(self.gridLayoutWidget_7)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_7.addWidget(self.label_56, 3, 4, 1, 1)

        self.label_58 = QLabel(self.gridLayoutWidget_7)
        self.label_58.setObjectName(u"label_58")

        self.gridLayout_7.addWidget(self.label_58, 2, 6, 1, 1)

        self.lineEdit_7 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_7, 1, 3, 1, 1)

        self.label_50 = QLabel(self.gridLayoutWidget_7)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_7.addWidget(self.label_50, 3, 0, 1, 1)

        self.lineEdit_14 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_14, 4, 1, 1, 1)

        self.lineEdit_12 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_12, 2, 7, 1, 1)

        self.lineEdit_10 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_10, 3, 5, 1, 1)

        self.lineEdit_17 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_17, 4, 7, 1, 1)

        self.label_62 = QLabel(self.gridLayoutWidget_7)
        self.label_62.setObjectName(u"label_62")

        self.gridLayout_7.addWidget(self.label_62, 4, 4, 1, 1)

        self.lineEdit_5 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_5, 3, 3, 1, 1)

        self.lineEdit_9 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_9, 2, 5, 1, 1)

        self.label_55 = QLabel(self.gridLayoutWidget_7)
        self.label_55.setObjectName(u"label_55")

        self.gridLayout_7.addWidget(self.label_55, 2, 4, 1, 1)

        self.label_16 = QLabel(self.gridLayoutWidget_7)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_7.addWidget(self.label_16, 1, 0, 1, 1)

        self.lineEdit_3 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_3, 2, 1, 1, 1)

        self.lineEdit_6 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_6, 2, 3, 1, 1)

        self.label_51 = QLabel(self.gridLayoutWidget_7)
        self.label_51.setObjectName(u"label_51")

        self.gridLayout_7.addWidget(self.label_51, 1, 2, 1, 1)

        self.label_63 = QLabel(self.gridLayoutWidget_7)
        self.label_63.setObjectName(u"label_63")

        self.gridLayout_7.addWidget(self.label_63, 4, 6, 1, 1)

        self.label_49 = QLabel(self.gridLayoutWidget_7)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_7.addWidget(self.label_49, 2, 0, 1, 1)

        self.label_60 = QLabel(self.gridLayoutWidget_7)
        self.label_60.setObjectName(u"label_60")

        self.gridLayout_7.addWidget(self.label_60, 4, 0, 1, 1)

        self.lineEdit_15 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_15, 4, 3, 1, 1)

        self.label_151 = QLabel(self.gridLayoutWidget_7)
        self.label_151.setObjectName(u"label_151")

        self.gridLayout_7.addWidget(self.label_151, 0, 0, 1, 1)

        self.lineEdit_55 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_55.setObjectName(u"lineEdit_55")
        self.lineEdit_55.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_55, 0, 1, 1, 1)

        self.label_152 = QLabel(self.gridLayoutWidget_7)
        self.label_152.setObjectName(u"label_152")

        self.gridLayout_7.addWidget(self.label_152, 0, 2, 1, 1)

        self.lineEdit_56 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_56.setObjectName(u"lineEdit_56")
        self.lineEdit_56.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_56, 0, 3, 1, 1)

        self.label_153 = QLabel(self.gridLayoutWidget_7)
        self.label_153.setObjectName(u"label_153")

        self.gridLayout_7.addWidget(self.label_153, 0, 4, 1, 1)

        self.lineEdit_57 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_57.setObjectName(u"lineEdit_57")
        self.lineEdit_57.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_57, 0, 5, 1, 1)

        self.label_154 = QLabel(self.gridLayoutWidget_7)
        self.label_154.setObjectName(u"label_154")

        self.gridLayout_7.addWidget(self.label_154, 0, 6, 1, 1)

        self.lineEdit_58 = QLineEdit(self.gridLayoutWidget_7)
        self.lineEdit_58.setObjectName(u"lineEdit_58")
        self.lineEdit_58.setEnabled(False)

        self.gridLayout_7.addWidget(self.lineEdit_58, 0, 7, 1, 1)

        self.gridLayoutWidget_13 = QWidget(self.page_2)
        self.gridLayoutWidget_13.setObjectName(u"gridLayoutWidget_13")
        self.gridLayoutWidget_13.setGeometry(QRect(0, 0, 241, 31))
        self.gridLayout_13 = QGridLayout(self.gridLayoutWidget_13)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_2 = QLineEdit(self.gridLayoutWidget_13)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_13.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        self.label_45 = QLabel(self.gridLayoutWidget_13)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_13.addWidget(self.label_45, 0, 0, 1, 1)

        self.number_of_planets_spinbox_lock_2 = LockUnlockButton(self.gridLayoutWidget_13)
        self.number_of_planets_spinbox_lock_2.setObjectName(u"number_of_planets_spinbox_lock_2")

        self.gridLayout_13.addWidget(self.number_of_planets_spinbox_lock_2, 0, 2, 1, 1)

        self.gridLayoutWidget_8 = QWidget(self.page_2)
        self.gridLayoutWidget_8.setObjectName(u"gridLayoutWidget_8")
        self.gridLayoutWidget_8.setGeometry(QRect(0, 30, 261, 61))
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

        self.gridLayoutWidget_6 = QWidget(self.page_2)
        self.gridLayoutWidget_6.setObjectName(u"gridLayoutWidget_6")
        self.gridLayoutWidget_6.setGeometry(QRect(0, 270, 447, 61))
        self.gridLayout_6 = QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_156 = QLabel(self.gridLayoutWidget_6)
        self.label_156.setObjectName(u"label_156")

        self.gridLayout_6.addWidget(self.label_156, 0, 4, 1, 1)

        self.lineEdit_61 = QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_61.setObjectName(u"lineEdit_61")
        self.lineEdit_61.setEnabled(False)

        self.gridLayout_6.addWidget(self.lineEdit_61, 0, 5, 1, 1)

        self.label_155 = QLabel(self.gridLayoutWidget_6)
        self.label_155.setObjectName(u"label_155")

        self.gridLayout_6.addWidget(self.label_155, 0, 2, 1, 1)

        self.lineEdit_60 = QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_60.setObjectName(u"lineEdit_60")
        self.lineEdit_60.setEnabled(False)

        self.gridLayout_6.addWidget(self.lineEdit_60, 0, 3, 1, 1)

        self.lineEdit_59 = QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_59.setObjectName(u"lineEdit_59")
        self.lineEdit_59.setEnabled(False)

        self.gridLayout_6.addWidget(self.lineEdit_59, 0, 1, 1, 1)

        self.label_17 = QLabel(self.gridLayoutWidget_6)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_6.addWidget(self.label_17, 0, 0, 1, 1)

        self.label_18 = QLabel(self.gridLayoutWidget_6)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_6.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_19 = QLabel(self.gridLayoutWidget_6)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 1, 2, 1, 1)

        self.label_25 = QLabel(self.gridLayoutWidget_6)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_6.addWidget(self.label_25, 1, 4, 1, 1)

        self.lineEdit_62 = QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_62.setObjectName(u"lineEdit_62")
        self.lineEdit_62.setEnabled(False)

        self.gridLayout_6.addWidget(self.lineEdit_62, 1, 1, 1, 1)

        self.lineEdit_63 = QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_63.setObjectName(u"lineEdit_63")
        self.lineEdit_63.setEnabled(False)

        self.gridLayout_6.addWidget(self.lineEdit_63, 1, 3, 1, 1)

        self.lineEdit_64 = QLineEdit(self.gridLayoutWidget_6)
        self.lineEdit_64.setObjectName(u"lineEdit_64")
        self.lineEdit_64.setEnabled(False)

        self.gridLayout_6.addWidget(self.lineEdit_64, 1, 5, 1, 1)

        self.gridLayoutWidget_9 = QWidget(self.page_2)
        self.gridLayoutWidget_9.setObjectName(u"gridLayoutWidget_9")
        self.gridLayoutWidget_9.setGeometry(QRect(0, 90, 261, 31))
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

        self.toolBox.addItem(self.page_2, u"Force Analysis")
        self.shape_page = QWidget()
        self.shape_page.setObjectName(u"shape_page")
        self.shape_page.setGeometry(QRect(0, 0, 461, 457))
        self.gridLayoutWidget_18 = QWidget(self.shape_page)
        self.gridLayoutWidget_18.setObjectName(u"gridLayoutWidget_18")
        self.gridLayoutWidget_18.setGeometry(QRect(10, 140, 311, 31))
        self.gridLayout_18 = QGridLayout(self.gridLayoutWidget_18)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_19 = QLineEdit(self.gridLayoutWidget_18)
        self.lineEdit_19.setObjectName(u"lineEdit_19")
        self.lineEdit_19.setEnabled(False)

        self.gridLayout_18.addWidget(self.lineEdit_19, 0, 1, 1, 1)

        self.label_69 = QLabel(self.gridLayoutWidget_18)
        self.label_69.setObjectName(u"label_69")

        self.gridLayout_18.addWidget(self.label_69, 0, 2, 1, 1)

        self.label_66 = QLabel(self.gridLayoutWidget_18)
        self.label_66.setObjectName(u"label_66")

        self.gridLayout_18.addWidget(self.label_66, 0, 0, 1, 1)

        self.lineEdit_21 = QLineEdit(self.gridLayoutWidget_18)
        self.lineEdit_21.setObjectName(u"lineEdit_21")
        self.lineEdit_21.setEnabled(False)

        self.gridLayout_18.addWidget(self.lineEdit_21, 0, 3, 1, 1)

        self.gridLayoutWidget_17 = QWidget(self.shape_page)
        self.gridLayoutWidget_17.setObjectName(u"gridLayoutWidget_17")
        self.gridLayoutWidget_17.setGeometry(QRect(10, 40, 311, 31))
        self.gridLayout_17 = QGridLayout(self.gridLayoutWidget_17)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_13 = QLineEdit(self.gridLayoutWidget_17)
        self.lineEdit_13.setObjectName(u"lineEdit_13")

        self.gridLayout_17.addWidget(self.lineEdit_13, 0, 1, 1, 1)

        self.label_67 = QLabel(self.gridLayoutWidget_17)
        self.label_67.setObjectName(u"label_67")

        self.gridLayout_17.addWidget(self.label_67, 0, 0, 1, 1)

        self.number_of_planets_spinbox_lock_3 = LockUnlockButton(self.gridLayoutWidget_17)
        self.number_of_planets_spinbox_lock_3.setObjectName(u"number_of_planets_spinbox_lock_3")

        self.gridLayout_17.addWidget(self.number_of_planets_spinbox_lock_3, 0, 2, 1, 1)

        self.gridLayoutWidget_21 = QWidget(self.shape_page)
        self.gridLayoutWidget_21.setObjectName(u"gridLayoutWidget_21")
        self.gridLayoutWidget_21.setGeometry(QRect(10, 260, 421, 31))
        self.gridLayout_21 = QGridLayout(self.gridLayoutWidget_21)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_25 = QLineEdit(self.gridLayoutWidget_21)
        self.lineEdit_25.setObjectName(u"lineEdit_25")
        self.lineEdit_25.setEnabled(False)

        self.gridLayout_21.addWidget(self.lineEdit_25, 0, 1, 1, 1)

        self.lineEdit_26 = QLineEdit(self.gridLayoutWidget_21)
        self.lineEdit_26.setObjectName(u"lineEdit_26")
        self.lineEdit_26.setEnabled(False)

        self.gridLayout_21.addWidget(self.lineEdit_26, 0, 3, 1, 1)

        self.lineEdit_27 = QLineEdit(self.gridLayoutWidget_21)
        self.lineEdit_27.setObjectName(u"lineEdit_27")
        self.lineEdit_27.setEnabled(False)

        self.gridLayout_21.addWidget(self.lineEdit_27, 0, 5, 1, 1)

        self.label_75 = QLabel(self.gridLayoutWidget_21)
        self.label_75.setObjectName(u"label_75")

        self.gridLayout_21.addWidget(self.label_75, 0, 2, 1, 1)

        self.label_76 = QLabel(self.gridLayoutWidget_21)
        self.label_76.setObjectName(u"label_76")

        self.gridLayout_21.addWidget(self.label_76, 0, 0, 1, 1)

        self.label_77 = QLabel(self.gridLayoutWidget_21)
        self.label_77.setObjectName(u"label_77")

        self.gridLayout_21.addWidget(self.label_77, 0, 4, 1, 1)

        self.gridLayoutWidget_19 = QWidget(self.shape_page)
        self.gridLayoutWidget_19.setObjectName(u"gridLayoutWidget_19")
        self.gridLayoutWidget_19.setGeometry(QRect(10, 70, 311, 31))
        self.gridLayout_19 = QGridLayout(self.gridLayoutWidget_19)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_23 = QLineEdit(self.gridLayoutWidget_19)
        self.lineEdit_23.setObjectName(u"lineEdit_23")

        self.gridLayout_19.addWidget(self.lineEdit_23, 0, 1, 1, 1)

        self.label_68 = QLabel(self.gridLayoutWidget_19)
        self.label_68.setObjectName(u"label_68")

        self.gridLayout_19.addWidget(self.label_68, 0, 0, 1, 1)

        self.number_of_planets_spinbox_lock_4 = LockUnlockButton(self.gridLayoutWidget_19)
        self.number_of_planets_spinbox_lock_4.setObjectName(u"number_of_planets_spinbox_lock_4")

        self.gridLayout_19.addWidget(self.number_of_planets_spinbox_lock_4, 0, 2, 1, 1)

        self.gridLayoutWidget_16 = QWidget(self.shape_page)
        self.gridLayoutWidget_16.setObjectName(u"gridLayoutWidget_16")
        self.gridLayoutWidget_16.setGeometry(QRect(10, 200, 421, 31))
        self.gridLayout_16 = QGridLayout(self.gridLayoutWidget_16)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_18 = QLineEdit(self.gridLayoutWidget_16)
        self.lineEdit_18.setObjectName(u"lineEdit_18")
        self.lineEdit_18.setEnabled(False)

        self.gridLayout_16.addWidget(self.lineEdit_18, 0, 1, 1, 1)

        self.lineEdit_20 = QLineEdit(self.gridLayoutWidget_16)
        self.lineEdit_20.setObjectName(u"lineEdit_20")
        self.lineEdit_20.setEnabled(False)

        self.gridLayout_16.addWidget(self.lineEdit_20, 0, 3, 1, 1)

        self.lineEdit_22 = QLineEdit(self.gridLayoutWidget_16)
        self.lineEdit_22.setObjectName(u"lineEdit_22")
        self.lineEdit_22.setEnabled(False)

        self.gridLayout_16.addWidget(self.lineEdit_22, 0, 5, 1, 1)

        self.label_73 = QLabel(self.gridLayoutWidget_16)
        self.label_73.setObjectName(u"label_73")

        self.gridLayout_16.addWidget(self.label_73, 0, 2, 1, 1)

        self.label_72 = QLabel(self.gridLayoutWidget_16)
        self.label_72.setObjectName(u"label_72")

        self.gridLayout_16.addWidget(self.label_72, 0, 0, 1, 1)

        self.label_74 = QLabel(self.gridLayoutWidget_16)
        self.label_74.setObjectName(u"label_74")

        self.gridLayout_16.addWidget(self.label_74, 0, 4, 1, 1)

        self.gridLayoutWidget_20 = QWidget(self.shape_page)
        self.gridLayoutWidget_20.setObjectName(u"gridLayoutWidget_20")
        self.gridLayoutWidget_20.setGeometry(QRect(10, 100, 311, 31))
        self.gridLayout_20 = QGridLayout(self.gridLayoutWidget_20)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_24 = QLineEdit(self.gridLayoutWidget_20)
        self.lineEdit_24.setObjectName(u"lineEdit_24")

        self.gridLayout_20.addWidget(self.lineEdit_24, 0, 1, 1, 1)

        self.label_70 = QLabel(self.gridLayoutWidget_20)
        self.label_70.setObjectName(u"label_70")

        self.gridLayout_20.addWidget(self.label_70, 0, 0, 1, 1)

        self.number_of_planets_spinbox_lock_5 = LockUnlockButton(self.gridLayoutWidget_20)
        self.number_of_planets_spinbox_lock_5.setObjectName(u"number_of_planets_spinbox_lock_5")

        self.gridLayout_20.addWidget(self.number_of_planets_spinbox_lock_5, 0, 2, 1, 1)

        self.gridLayoutWidget_5 = QWidget(self.shape_page)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(10, 10, 329, 31))
        self.gridLayout_5 = QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(self.gridLayoutWidget_5)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)

        self.comboBox = QComboBox(self.gridLayoutWidget_5)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_5.addWidget(self.comboBox, 0, 1, 1, 1)

        self.number_of_planets_spinbox_lock_11 = QToolButton(self.gridLayoutWidget_5)
        self.number_of_planets_spinbox_lock_11.setObjectName(u"number_of_planets_spinbox_lock_11")

        self.gridLayout_5.addWidget(self.number_of_planets_spinbox_lock_11, 0, 2, 1, 1)

        self.number_of_planets_spinbox_lock_12 = QToolButton(self.gridLayoutWidget_5)
        self.number_of_planets_spinbox_lock_12.setObjectName(u"number_of_planets_spinbox_lock_12")

        self.gridLayout_5.addWidget(self.number_of_planets_spinbox_lock_12, 0, 3, 1, 1)

        self.label_12 = QLabel(self.shape_page)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 180, 91, 17))
        self.label_13 = QLabel(self.shape_page)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 240, 91, 17))
        self.gridLayoutWidget_10 = QWidget(self.shape_page)
        self.gridLayoutWidget_10.setObjectName(u"gridLayoutWidget_10")
        self.gridLayoutWidget_10.setGeometry(QRect(10, 290, 211, 61))
        self.gridLayout_10 = QGridLayout(self.gridLayoutWidget_10)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_157 = QLabel(self.gridLayoutWidget_10)
        self.label_157.setObjectName(u"label_157")

        self.gridLayout_10.addWidget(self.label_157, 0, 0, 1, 1)

        self.actual_module_lineedit = QLengthEdit(self.gridLayoutWidget_10)
        self.actual_module_lineedit.setObjectName(u"actual_module_lineedit")
        self.actual_module_lineedit.setEnabled(True)

        self.gridLayout_10.addWidget(self.actual_module_lineedit, 0, 1, 1, 1)

        self.label_158 = QLabel(self.gridLayoutWidget_10)
        self.label_158.setObjectName(u"label_158")

        self.gridLayout_10.addWidget(self.label_158, 1, 0, 1, 1)

        self.actual_height_lineedit = QLengthEdit(self.gridLayoutWidget_10)
        self.actual_height_lineedit.setObjectName(u"actual_height_lineedit")
        self.actual_height_lineedit.setEnabled(True)

        self.gridLayout_10.addWidget(self.actual_height_lineedit, 1, 1, 1, 1)

        self.actual_module_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_10)
        self.actual_module_lineedit_lock.setObjectName(u"actual_module_lineedit_lock")

        self.gridLayout_10.addWidget(self.actual_module_lineedit_lock, 0, 2, 1, 1)

        self.actual_height_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_10)
        self.actual_height_lineedit_lock.setObjectName(u"actual_height_lineedit_lock")

        self.gridLayout_10.addWidget(self.actual_height_lineedit_lock, 1, 2, 1, 1)

        self.gridLayoutWidget_43 = QWidget(self.shape_page)
        self.gridLayoutWidget_43.setObjectName(u"gridLayoutWidget_43")
        self.gridLayoutWidget_43.setGeometry(QRect(10, 350, 211, 61))
        self.gridLayout_43 = QGridLayout(self.gridLayoutWidget_43)
        self.gridLayout_43.setObjectName(u"gridLayout_43")
        self.gridLayout_43.setContentsMargins(0, 0, 0, 0)
        self.label_159 = QLabel(self.gridLayoutWidget_43)
        self.label_159.setObjectName(u"label_159")

        self.gridLayout_43.addWidget(self.label_159, 0, 0, 1, 1)

        self.label_160 = QLabel(self.gridLayoutWidget_43)
        self.label_160.setObjectName(u"label_160")

        self.gridLayout_43.addWidget(self.label_160, 1, 0, 1, 1)

        self.lineEdit_67 = QLineEdit(self.gridLayoutWidget_43)
        self.lineEdit_67.setObjectName(u"lineEdit_67")
        self.lineEdit_67.setEnabled(False)

        self.gridLayout_43.addWidget(self.lineEdit_67, 0, 1, 1, 1)

        self.lineEdit_68 = QLineEdit(self.gridLayoutWidget_43)
        self.lineEdit_68.setObjectName(u"lineEdit_68")
        self.lineEdit_68.setEnabled(False)

        self.gridLayout_43.addWidget(self.lineEdit_68, 1, 1, 1, 1)

        self.toolBox.addItem(self.shape_page, u"Material and Height Requirements")

        self.retranslateUi(Dialog)

        self.toolBox.setCurrentIndex(3)
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
        self.label_54.setText(QCoreApplication.translate("Dialog", u"Ring Ft", None))
        self.label_61.setText(QCoreApplication.translate("Dialog", u"Planet Fn", None))
        self.label_57.setText(QCoreApplication.translate("Dialog", u"Carrier Ft", None))
        self.label_52.setText(QCoreApplication.translate("Dialog", u"Planet Fr", None))
        self.label_59.setText(QCoreApplication.translate("Dialog", u"Carrier Fa", None))
        self.label_53.setText(QCoreApplication.translate("Dialog", u"Planet Fa", None))
        self.label_64.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_56.setText(QCoreApplication.translate("Dialog", u"Ring Fa", None))
        self.label_58.setText(QCoreApplication.translate("Dialog", u"Carrier Fr", None))
        self.label_50.setText(QCoreApplication.translate("Dialog", u"Sun Fa", None))
        self.label_62.setText(QCoreApplication.translate("Dialog", u"Ring Fn", None))
        self.label_55.setText(QCoreApplication.translate("Dialog", u"Ring Fr", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Sun Ft", None))
        self.label_51.setText(QCoreApplication.translate("Dialog", u"Planet Ft", None))
        self.label_63.setText(QCoreApplication.translate("Dialog", u"Carrier Fn", None))
        self.label_49.setText(QCoreApplication.translate("Dialog", u"Sun Fr", None))
        self.label_60.setText(QCoreApplication.translate("Dialog", u"Sun Fn", None))
        self.label_151.setText(QCoreApplication.translate("Dialog", u"Sun T", None))
        self.label_152.setText(QCoreApplication.translate("Dialog", u"Planet T", None))
        self.label_153.setText(QCoreApplication.translate("Dialog", u"Ring T", None))
        self.label_154.setText(QCoreApplication.translate("Dialog", u"Carrier T", None))
        self.label_45.setText(QCoreApplication.translate("Dialog", u"Max Input Torque:", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Beta:", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"Double Helix:", None))
        self.double_helix_checkbox.setText("")
        self.label_156.setText(QCoreApplication.translate("Dialog", u"Ring Zy", None))
        self.label_155.setText(QCoreApplication.translate("Dialog", u"Planet Zy", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"Sun Zy", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"Sun form factor", None))
        self.label_19.setText(QCoreApplication.translate("Dialog", u"Planet form factor", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"Ring form factor", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"Pressure Angle:", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("Dialog", u"Force Analysis", None))
        self.label_69.setText(QCoreApplication.translate("Dialog", u"min module", None))
        self.label_66.setText(QCoreApplication.translate("Dialog", u"Max Module", None))
        self.label_67.setText(QCoreApplication.translate("Dialog", u"Max Bend Stress (\u03c3b, ~0.66*Yield)", None))
        self.label_75.setText(QCoreApplication.translate("Dialog", u"Planet min h", None))
        self.label_76.setText(QCoreApplication.translate("Dialog", u"Sun min h", None))
        self.label_77.setText(QCoreApplication.translate("Dialog", u"Ring min h", None))
        self.label_68.setText(QCoreApplication.translate("Dialog", u"Elastic Modulus:", None))
        self.label_73.setText(QCoreApplication.translate("Dialog", u"Planet min h", None))
        self.label_72.setText(QCoreApplication.translate("Dialog", u"Sun min h", None))
        self.label_74.setText(QCoreApplication.translate("Dialog", u"Ring min h", None))
        self.label_70.setText(QCoreApplication.translate("Dialog", u"Poisson Ratio:", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Material", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Bending Stress:", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Contact Stress:", None))
        self.label_157.setText(QCoreApplication.translate("Dialog", u"Actual Module", None))
        self.label_158.setText(QCoreApplication.translate("Dialog", u"Actual Height", None))
        self.label_159.setText(QCoreApplication.translate("Dialog", u"Actual Max Input Torque", None))
        self.label_160.setText(QCoreApplication.translate("Dialog", u"Safety Factor", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.shape_page), QCoreApplication.translate("Dialog", u"Material and Height Requirements", None))
    # retranslateUi

