# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gear-selectorsNUyAQv.ui'
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
from .object_combobox import ObjectComboBox
from .torque_ui import QTorqueEdit
from .force_ui import QForceEdit


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(477, 564)
        self.toolBox = QToolBox(Dialog)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setGeometry(QRect(10, 20, 461, 531))
        self.min_max_teeth_page = QWidget()
        self.min_max_teeth_page.setObjectName(u"min_max_teeth_page")
        self.min_max_teeth_page.setGeometry(QRect(0, 0, 461, 407))
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
        self.planetary_ratio_page.setGeometry(QRect(0, 0, 461, 407))
        self.gridLayoutWidget_3 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 150, 385, 101))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gear_ratio_options_abort = QPushButton(self.gridLayoutWidget_3)
        self.gear_ratio_options_abort.setObjectName(u"gear_ratio_options_abort")

        self.gridLayout_3.addWidget(self.gear_ratio_options_abort, 2, 3, 1, 1)

        self.label_65 = QLabel(self.gridLayoutWidget_3)
        self.label_65.setObjectName(u"label_65")
        self.label_65.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_65, 1, 2, 1, 1)

        self.label_24 = QLabel(self.gridLayoutWidget_3)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_3.addWidget(self.label_24, 1, 3, 1, 1)

        self.gear_ratio_options_progress = QProgressBar(self.gridLayoutWidget_3)
        self.gear_ratio_options_progress.setObjectName(u"gear_ratio_options_progress")
        self.gear_ratio_options_progress.setValue(100)

        self.gridLayout_3.addWidget(self.gear_ratio_options_progress, 2, 1, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.target_inverse_gear_ratio_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_3)
        self.target_inverse_gear_ratio_lineedit_lock.setObjectName(u"target_inverse_gear_ratio_lineedit_lock")
        self.target_inverse_gear_ratio_lineedit_lock.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_3.addWidget(self.target_inverse_gear_ratio_lineedit_lock, 0, 2, 1, 1)

        self.label_20 = QLabel(self.gridLayoutWidget_3)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_3.addWidget(self.label_20, 1, 0, 1, 1)

        self.target_gear_ratio_lineedit = QFractionEdit(self.gridLayoutWidget_3)
        self.target_gear_ratio_lineedit.setObjectName(u"target_gear_ratio_lineedit")

        self.gridLayout_3.addWidget(self.target_gear_ratio_lineedit, 1, 1, 1, 1)

        self.label_26 = QLabel(self.gridLayoutWidget_3)
        self.label_26.setObjectName(u"label_26")

        self.gridLayout_3.addWidget(self.label_26, 0, 3, 1, 1)

        self.target_inverse_gear_ratio_lineedit = QFractionEdit(self.gridLayoutWidget_3)
        self.target_inverse_gear_ratio_lineedit.setObjectName(u"target_inverse_gear_ratio_lineedit")

        self.gridLayout_3.addWidget(self.target_inverse_gear_ratio_lineedit, 0, 1, 1, 1)

        self.gear_ratio_options_calculate = QPushButton(self.gridLayoutWidget_3)
        self.gear_ratio_options_calculate.setObjectName(u"gear_ratio_options_calculate")

        self.gridLayout_3.addWidget(self.gear_ratio_options_calculate, 2, 2, 1, 1)

        self.gridLayoutWidget_4 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 330, 360, 61))
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_36 = QLabel(self.gridLayoutWidget_4)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_4.addWidget(self.label_36, 0, 0, 1, 1)

        self.label_37 = QLabel(self.gridLayoutWidget_4)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_4.addWidget(self.label_37, 1, 0, 1, 1)

        self.checkBox = QCheckBox(self.gridLayoutWidget_4)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setEnabled(False)
        self.checkBox.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox, 0, 1, 1, 1)

        self.checkBox_2 = QCheckBox(self.gridLayoutWidget_4)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setEnabled(False)
        self.checkBox_2.setChecked(True)

        self.gridLayout_4.addWidget(self.checkBox_2, 1, 1, 1, 1)

        self.gridLayoutWidget_2 = QWidget(self.planetary_ratio_page)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 0, 231, 145))
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
        self.gridLayoutWidget_11.setGeometry(QRect(10, 260, 421, 31))
        self.gridLayout_11 = QGridLayout(self.gridLayoutWidget_11)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gear_ratio_options_combobox = ObjectComboBox(self.gridLayoutWidget_11)
        self.gear_ratio_options_combobox.setObjectName(u"gear_ratio_options_combobox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gear_ratio_options_combobox.sizePolicy().hasHeightForWidth())
        self.gear_ratio_options_combobox.setSizePolicy(sizePolicy)

        self.gridLayout_11.addWidget(self.gear_ratio_options_combobox, 0, 1, 1, 1)

        self.gear_ratio_options_combobox_lock = LockUnlockButton(self.gridLayoutWidget_11)
        self.gear_ratio_options_combobox_lock.setObjectName(u"gear_ratio_options_combobox_lock")

        self.gridLayout_11.addWidget(self.gear_ratio_options_combobox_lock, 0, 2, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget_11)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)

        self.gridLayout_11.addWidget(self.label_8, 0, 0, 1, 1)

        self.toolBox.addItem(self.planetary_ratio_page, u"Planetary Ratio Calculator")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 461, 407))
        self.gridLayoutWidget_7 = QWidget(self.page_2)
        self.gridLayoutWidget_7.setObjectName(u"gridLayoutWidget_7")
        self.gridLayoutWidget_7.setGeometry(QRect(0, 220, 441, 121))
        self.gridLayout_7 = QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_62 = QLabel(self.gridLayoutWidget_7)
        self.label_62.setObjectName(u"label_62")

        self.gridLayout_7.addWidget(self.label_62, 3, 4, 1, 1)

        self.sun_fa_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.sun_fa_lineedit.setObjectName(u"sun_fa_lineedit")
        self.sun_fa_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.sun_fa_lineedit, 2, 1, 1, 1)

        self.label_57 = QLabel(self.gridLayoutWidget_7)
        self.label_57.setObjectName(u"label_57")

        self.gridLayout_7.addWidget(self.label_57, 0, 6, 1, 1)

        self.carrier_fr_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.carrier_fr_lineedit.setObjectName(u"carrier_fr_lineedit")
        self.carrier_fr_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.carrier_fr_lineedit, 1, 7, 1, 1)

        self.label_59 = QLabel(self.gridLayoutWidget_7)
        self.label_59.setObjectName(u"label_59")

        self.gridLayout_7.addWidget(self.label_59, 2, 6, 1, 1)

        self.label_64 = QLabel(self.gridLayoutWidget_7)
        self.label_64.setObjectName(u"label_64")
        self.label_64.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_64, 2, 7, 1, 1)

        self.label_54 = QLabel(self.gridLayoutWidget_7)
        self.label_54.setObjectName(u"label_54")

        self.gridLayout_7.addWidget(self.label_54, 0, 4, 1, 1)

        self.sun_fr_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.sun_fr_lineedit.setObjectName(u"sun_fr_lineedit")
        self.sun_fr_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.sun_fr_lineedit, 1, 1, 1, 1)

        self.label_60 = QLabel(self.gridLayoutWidget_7)
        self.label_60.setObjectName(u"label_60")

        self.gridLayout_7.addWidget(self.label_60, 3, 0, 1, 1)

        self.label_16 = QLabel(self.gridLayoutWidget_7)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_7.addWidget(self.label_16, 0, 0, 1, 1)

        self.carrier_fn_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.carrier_fn_lineedit.setObjectName(u"carrier_fn_lineedit")
        self.carrier_fn_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.carrier_fn_lineedit, 3, 7, 1, 1)

        self.planet_fn_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.planet_fn_lineedit.setObjectName(u"planet_fn_lineedit")
        self.planet_fn_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.planet_fn_lineedit, 3, 3, 1, 1)

        self.ring_fa_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.ring_fa_lineedit.setObjectName(u"ring_fa_lineedit")
        self.ring_fa_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.ring_fa_lineedit, 2, 5, 1, 1)

        self.sun_fn_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.sun_fn_lineedit.setObjectName(u"sun_fn_lineedit")
        self.sun_fn_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.sun_fn_lineedit, 3, 1, 1, 1)

        self.carrier_ft_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.carrier_ft_lineedit.setObjectName(u"carrier_ft_lineedit")
        self.carrier_ft_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.carrier_ft_lineedit, 0, 7, 1, 1)

        self.label_50 = QLabel(self.gridLayoutWidget_7)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_7.addWidget(self.label_50, 2, 0, 1, 1)

        self.ring_fn_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.ring_fn_lineedit.setObjectName(u"ring_fn_lineedit")
        self.ring_fn_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.ring_fn_lineedit, 3, 5, 1, 1)

        self.ring_ft_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.ring_ft_lineedit.setObjectName(u"ring_ft_lineedit")
        self.ring_ft_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.ring_ft_lineedit, 0, 5, 1, 1)

        self.label_58 = QLabel(self.gridLayoutWidget_7)
        self.label_58.setObjectName(u"label_58")

        self.gridLayout_7.addWidget(self.label_58, 1, 6, 1, 1)

        self.sun_ft_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.sun_ft_lineedit.setObjectName(u"sun_ft_lineedit")
        self.sun_ft_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.sun_ft_lineedit, 0, 1, 1, 1)

        self.label_56 = QLabel(self.gridLayoutWidget_7)
        self.label_56.setObjectName(u"label_56")

        self.gridLayout_7.addWidget(self.label_56, 2, 4, 1, 1)

        self.label_63 = QLabel(self.gridLayoutWidget_7)
        self.label_63.setObjectName(u"label_63")

        self.gridLayout_7.addWidget(self.label_63, 3, 6, 1, 1)

        self.ring_fr_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.ring_fr_lineedit.setObjectName(u"ring_fr_lineedit")
        self.ring_fr_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.ring_fr_lineedit, 1, 5, 1, 1)

        self.label_55 = QLabel(self.gridLayoutWidget_7)
        self.label_55.setObjectName(u"label_55")

        self.gridLayout_7.addWidget(self.label_55, 1, 4, 1, 1)

        self.label_49 = QLabel(self.gridLayoutWidget_7)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_7.addWidget(self.label_49, 1, 0, 1, 1)

        self.label_61 = QLabel(self.gridLayoutWidget_7)
        self.label_61.setObjectName(u"label_61")

        self.gridLayout_7.addWidget(self.label_61, 3, 2, 1, 1)

        self.planet_fa_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.planet_fa_lineedit.setObjectName(u"planet_fa_lineedit")
        self.planet_fa_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.planet_fa_lineedit, 2, 3, 1, 1)

        self.label_53 = QLabel(self.gridLayoutWidget_7)
        self.label_53.setObjectName(u"label_53")

        self.gridLayout_7.addWidget(self.label_53, 2, 2, 1, 1)

        self.planet_fr_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.planet_fr_lineedit.setObjectName(u"planet_fr_lineedit")
        self.planet_fr_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.planet_fr_lineedit, 1, 3, 1, 1)

        self.label_52 = QLabel(self.gridLayoutWidget_7)
        self.label_52.setObjectName(u"label_52")

        self.gridLayout_7.addWidget(self.label_52, 1, 2, 1, 1)

        self.planet_ft_lineedit = QForceEdit(self.gridLayoutWidget_7)
        self.planet_ft_lineedit.setObjectName(u"planet_ft_lineedit")
        self.planet_ft_lineedit.setEnabled(False)

        self.gridLayout_7.addWidget(self.planet_ft_lineedit, 0, 3, 1, 1)

        self.label_51 = QLabel(self.gridLayoutWidget_7)
        self.label_51.setObjectName(u"label_51")

        self.gridLayout_7.addWidget(self.label_51, 0, 2, 1, 1)

        self.gridLayoutWidget_13 = QWidget(self.page_2)
        self.gridLayoutWidget_13.setObjectName(u"gridLayoutWidget_13")
        self.gridLayoutWidget_13.setGeometry(QRect(0, 0, 241, 31))
        self.gridLayout_13 = QGridLayout(self.gridLayoutWidget_13)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.max_in_torque_lineedit = QTorqueEdit(self.gridLayoutWidget_13)
        self.max_in_torque_lineedit.setObjectName(u"max_in_torque_lineedit")

        self.gridLayout_13.addWidget(self.max_in_torque_lineedit, 0, 1, 1, 1)

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
        self.gridLayoutWidget_6.setGeometry(QRect(0, 340, 447, 61))
        self.gridLayout_6 = QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_156 = QLabel(self.gridLayoutWidget_6)
        self.label_156.setObjectName(u"label_156")

        self.gridLayout_6.addWidget(self.label_156, 0, 4, 1, 1)

        self.ring_zy_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.ring_zy_lineedit.setObjectName(u"ring_zy_lineedit")
        self.ring_zy_lineedit.setEnabled(False)

        self.gridLayout_6.addWidget(self.ring_zy_lineedit, 0, 5, 1, 1)

        self.label_155 = QLabel(self.gridLayoutWidget_6)
        self.label_155.setObjectName(u"label_155")

        self.gridLayout_6.addWidget(self.label_155, 0, 2, 1, 1)

        self.planet_zy_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.planet_zy_lineedit.setObjectName(u"planet_zy_lineedit")
        self.planet_zy_lineedit.setEnabled(False)

        self.gridLayout_6.addWidget(self.planet_zy_lineedit, 0, 3, 1, 1)

        self.sun_zy_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.sun_zy_lineedit.setObjectName(u"sun_zy_lineedit")
        self.sun_zy_lineedit.setEnabled(False)

        self.gridLayout_6.addWidget(self.sun_zy_lineedit, 0, 1, 1, 1)

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

        self.sun_form_factor_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.sun_form_factor_lineedit.setObjectName(u"sun_form_factor_lineedit")
        self.sun_form_factor_lineedit.setEnabled(False)

        self.gridLayout_6.addWidget(self.sun_form_factor_lineedit, 1, 1, 1, 1)

        self.planet_form_factor_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.planet_form_factor_lineedit.setObjectName(u"planet_form_factor_lineedit")
        self.planet_form_factor_lineedit.setEnabled(False)

        self.gridLayout_6.addWidget(self.planet_form_factor_lineedit, 1, 3, 1, 1)

        self.ring_form_factor_lineedit = QLineEdit(self.gridLayoutWidget_6)
        self.ring_form_factor_lineedit.setObjectName(u"ring_form_factor_lineedit")
        self.ring_form_factor_lineedit.setEnabled(False)

        self.gridLayout_6.addWidget(self.ring_form_factor_lineedit, 1, 5, 1, 1)

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

        self.gridLayoutWidget_22 = QWidget(self.page_2)
        self.gridLayoutWidget_22.setObjectName(u"gridLayoutWidget_22")
        self.gridLayoutWidget_22.setGeometry(QRect(0, 160, 441, 31))
        self.gridLayout_22 = QGridLayout(self.gridLayoutWidget_22)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.label_151 = QLabel(self.gridLayoutWidget_22)
        self.label_151.setObjectName(u"label_151")

        self.gridLayout_22.addWidget(self.label_151, 0, 0, 1, 1)

        self.label_152 = QLabel(self.gridLayoutWidget_22)
        self.label_152.setObjectName(u"label_152")

        self.gridLayout_22.addWidget(self.label_152, 0, 2, 1, 1)

        self.planet_t_lineedit = QTorqueEdit(self.gridLayoutWidget_22)
        self.planet_t_lineedit.setObjectName(u"planet_t_lineedit")
        self.planet_t_lineedit.setEnabled(False)

        self.gridLayout_22.addWidget(self.planet_t_lineedit, 0, 3, 1, 1)

        self.label_153 = QLabel(self.gridLayoutWidget_22)
        self.label_153.setObjectName(u"label_153")

        self.gridLayout_22.addWidget(self.label_153, 0, 4, 1, 1)

        self.sun_t_lineedit = QTorqueEdit(self.gridLayoutWidget_22)
        self.sun_t_lineedit.setObjectName(u"sun_t_lineedit")
        self.sun_t_lineedit.setEnabled(False)

        self.gridLayout_22.addWidget(self.sun_t_lineedit, 0, 1, 1, 1)

        self.label_154 = QLabel(self.gridLayoutWidget_22)
        self.label_154.setObjectName(u"label_154")

        self.gridLayout_22.addWidget(self.label_154, 0, 6, 1, 1)

        self.ring_t_lineedit = QTorqueEdit(self.gridLayoutWidget_22)
        self.ring_t_lineedit.setObjectName(u"ring_t_lineedit")
        self.ring_t_lineedit.setEnabled(False)

        self.gridLayout_22.addWidget(self.ring_t_lineedit, 0, 5, 1, 1)

        self.carrier_t_lineedit = QTorqueEdit(self.gridLayoutWidget_22)
        self.carrier_t_lineedit.setObjectName(u"carrier_t_lineedit")
        self.carrier_t_lineedit.setEnabled(False)

        self.gridLayout_22.addWidget(self.carrier_t_lineedit, 0, 7, 1, 1)

        self.gridLayoutWidget_23 = QWidget(self.page_2)
        self.gridLayoutWidget_23.setObjectName(u"gridLayoutWidget_23")
        self.gridLayoutWidget_23.setGeometry(QRect(0, 190, 441, 31))
        self.gridLayout_23 = QGridLayout(self.gridLayoutWidget_23)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_23.setContentsMargins(0, 0, 0, 0)
        self.label_161 = QLabel(self.gridLayoutWidget_23)
        self.label_161.setObjectName(u"label_161")

        self.gridLayout_23.addWidget(self.label_161, 0, 0, 1, 1)

        self.load_sharing_planets_lineedit = QLineEdit(self.gridLayoutWidget_23)
        self.load_sharing_planets_lineedit.setObjectName(u"load_sharing_planets_lineedit")
        self.load_sharing_planets_lineedit.setEnabled(False)

        self.gridLayout_23.addWidget(self.load_sharing_planets_lineedit, 0, 1, 1, 1)

        self.gridLayoutWidget_24 = QWidget(self.page_2)
        self.gridLayoutWidget_24.setObjectName(u"gridLayoutWidget_24")
        self.gridLayoutWidget_24.setGeometry(QRect(0, 120, 441, 31))
        self.gridLayout_24 = QGridLayout(self.gridLayoutWidget_24)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(0, 0, 0, 0)
        self.label_162 = QLabel(self.gridLayoutWidget_24)
        self.label_162.setObjectName(u"label_162")

        self.gridLayout_24.addWidget(self.label_162, 0, 0, 1, 1)

        self.actual_module_slider = QSlider(self.gridLayoutWidget_24)
        self.actual_module_slider.setObjectName(u"actual_module_slider")
        sizePolicy.setHeightForWidth(self.actual_module_slider.sizePolicy().hasHeightForWidth())
        self.actual_module_slider.setSizePolicy(sizePolicy)
        self.actual_module_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_24.addWidget(self.actual_module_slider, 0, 1, 1, 1)

        self.actual_module_lineedit_lock = LockUnlockButton(self.gridLayoutWidget_24)
        self.actual_module_lineedit_lock.setObjectName(u"actual_module_lineedit_lock")

        self.gridLayout_24.addWidget(self.actual_module_lineedit_lock, 0, 3, 1, 1)

        self.actual_module_lineedit = QLengthEdit(self.gridLayoutWidget_24)
        self.actual_module_lineedit.setObjectName(u"actual_module_lineedit")
        self.actual_module_lineedit.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.actual_module_lineedit.sizePolicy().hasHeightForWidth())
        self.actual_module_lineedit.setSizePolicy(sizePolicy2)

        self.gridLayout_24.addWidget(self.actual_module_lineedit, 0, 2, 1, 1)

        self.toolBox.addItem(self.page_2, u"Force Analysis")
        self.shape_page = QWidget()
        self.shape_page.setObjectName(u"shape_page")
        self.shape_page.setGeometry(QRect(0, 0, 461, 407))
        self.gridLayoutWidget_5 = QWidget(self.shape_page)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(0, 170, 341, 31))
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

        self.gridLayoutWidget_17 = QWidget(self.shape_page)
        self.gridLayoutWidget_17.setObjectName(u"gridLayoutWidget_17")
        self.gridLayoutWidget_17.setGeometry(QRect(0, 200, 311, 31))
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

        self.gridLayoutWidget_43 = QWidget(self.shape_page)
        self.gridLayoutWidget_43.setObjectName(u"gridLayoutWidget_43")
        self.gridLayoutWidget_43.setGeometry(QRect(0, 310, 211, 61))
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

        self.gridLayoutWidget_20 = QWidget(self.shape_page)
        self.gridLayoutWidget_20.setObjectName(u"gridLayoutWidget_20")
        self.gridLayoutWidget_20.setGeometry(QRect(0, 260, 311, 31))
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

        self.gridLayoutWidget_19 = QWidget(self.shape_page)
        self.gridLayoutWidget_19.setObjectName(u"gridLayoutWidget_19")
        self.gridLayoutWidget_19.setGeometry(QRect(0, 230, 311, 31))
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

        self.gridLayoutWidget_21 = QWidget(self.shape_page)
        self.gridLayoutWidget_21.setObjectName(u"gridLayoutWidget_21")
        self.gridLayoutWidget_21.setGeometry(QRect(0, 130, 421, 31))
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

        self.label_13 = QLabel(self.shape_page)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(0, 110, 111, 17))
        self.gridLayoutWidget_16 = QWidget(self.shape_page)
        self.gridLayoutWidget_16.setObjectName(u"gridLayoutWidget_16")
        self.gridLayoutWidget_16.setGeometry(QRect(0, 70, 421, 31))
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

        self.label_12 = QLabel(self.shape_page)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(0, 50, 91, 17))
        self.gridLayoutWidget_10 = QWidget(self.shape_page)
        self.gridLayoutWidget_10.setObjectName(u"gridLayoutWidget_10")
        self.gridLayoutWidget_10.setGeometry(QRect(0, 10, 421, 31))
        self.gridLayout_10 = QGridLayout(self.gridLayoutWidget_10)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_163 = QLabel(self.gridLayoutWidget_10)
        self.label_163.setObjectName(u"label_163")

        self.gridLayout_10.addWidget(self.label_163, 0, 0, 1, 1)

        self.horizontalSlider_2 = QSlider(self.gridLayoutWidget_10)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.gridLayout_10.addWidget(self.horizontalSlider_2, 0, 1, 1, 1)

        self.actual_height_lineedit_2 = QLengthEdit(self.gridLayoutWidget_10)
        self.actual_height_lineedit_2.setObjectName(u"actual_height_lineedit_2")
        self.actual_height_lineedit_2.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.actual_height_lineedit_2.sizePolicy().hasHeightForWidth())
        self.actual_height_lineedit_2.setSizePolicy(sizePolicy2)

        self.gridLayout_10.addWidget(self.actual_height_lineedit_2, 0, 2, 1, 1)

        self.actual_height_lineedit_lock_2 = LockUnlockButton(self.gridLayoutWidget_10)
        self.actual_height_lineedit_lock_2.setObjectName(u"actual_height_lineedit_lock_2")

        self.gridLayout_10.addWidget(self.actual_height_lineedit_lock_2, 0, 3, 1, 1)

        self.toolBox.addItem(self.shape_page, u"Material and Height Requirements")

        self.retranslateUi(Dialog)

        self.toolBox.setCurrentIndex(2)
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
        self.gear_ratio_options_abort.setText(QCoreApplication.translate("Dialog", u"Abort", None))
#if QT_CONFIG(tooltip)
        self.label_65.setToolTip(QCoreApplication.translate("Dialog", u"This entry sets or is set by sun torque", None))
#endif // QT_CONFIG(tooltip)
        self.label_65.setText(QCoreApplication.translate("Dialog", u"  =  ", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"Gear Ratio R", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Calculating Options:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Out-RPM / In-RPM", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"Out-T / In-T", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u"R\u207b\u00b9", None))
        self.gear_ratio_options_calculate.setText(QCoreApplication.translate("Dialog", u"Calculate", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"Satisfy Planet Neighbor Constraint:", None))
        self.label_37.setText(QCoreApplication.translate("Dialog", u"Satisfy Homogeneity Distribution Constraint:", None))
        self.checkBox.setText("")
        self.checkBox_2.setText("")
        self.label_34.setText(QCoreApplication.translate("Dialog", u"Planet Clearance:", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"Number of Planets:", None))
        self.label_35.setText(QCoreApplication.translate("Dialog", u"Gear Addendum:", None))
        self.label_43.setText(QCoreApplication.translate("Dialog", u"Number of Options:", None))
        self.label_44.setText(QCoreApplication.translate("Dialog", u"Use Absolute Value:", None))
        self.use_abs_checkbox.setText("")
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Options:", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.planetary_ratio_page), QCoreApplication.translate("Dialog", u"Planetary Ratio Calculator", None))
        self.label_62.setText(QCoreApplication.translate("Dialog", u"Ring Fn", None))
        self.label_57.setText(QCoreApplication.translate("Dialog", u"Carrier Ft", None))
        self.label_59.setText(QCoreApplication.translate("Dialog", u"Carrier Fa", None))
        self.label_64.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.label_54.setText(QCoreApplication.translate("Dialog", u"Ring Ft", None))
        self.label_60.setText(QCoreApplication.translate("Dialog", u"Sun Fn", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Sun Ft", None))
        self.label_50.setText(QCoreApplication.translate("Dialog", u"Sun Fa", None))
        self.label_58.setText(QCoreApplication.translate("Dialog", u"Carrier Fr", None))
        self.label_56.setText(QCoreApplication.translate("Dialog", u"Ring Fa", None))
        self.label_63.setText(QCoreApplication.translate("Dialog", u"Carrier Fn", None))
        self.label_55.setText(QCoreApplication.translate("Dialog", u"Ring Fr", None))
        self.label_49.setText(QCoreApplication.translate("Dialog", u"Sun Fr", None))
        self.label_61.setText(QCoreApplication.translate("Dialog", u"Planet Fn", None))
        self.label_53.setText(QCoreApplication.translate("Dialog", u"Planet Fa", None))
        self.label_52.setText(QCoreApplication.translate("Dialog", u"Planet Fr", None))
        self.label_51.setText(QCoreApplication.translate("Dialog", u"Planet Ft", None))
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
        self.label_151.setText(QCoreApplication.translate("Dialog", u"Sun T", None))
        self.label_152.setText(QCoreApplication.translate("Dialog", u"Planet T", None))
        self.label_153.setText(QCoreApplication.translate("Dialog", u"Ring T", None))
        self.label_154.setText(QCoreApplication.translate("Dialog", u"Carrier T", None))
        self.label_161.setText(QCoreApplication.translate("Dialog", u"Num planets / load sharing:", None))
        self.label_162.setText(QCoreApplication.translate("Dialog", u"Actual Module", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("Dialog", u"Force Analysis", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Material", None))
        self.label_67.setText(QCoreApplication.translate("Dialog", u"Max Bend Stress (\u03c3b, ~0.66*Yield)", None))
        self.label_159.setText(QCoreApplication.translate("Dialog", u"Actual Max Input Torque", None))
        self.label_160.setText(QCoreApplication.translate("Dialog", u"Safety Factor", None))
        self.label_70.setText(QCoreApplication.translate("Dialog", u"Poisson Ratio:", None))
        self.label_68.setText(QCoreApplication.translate("Dialog", u"Elastic Modulus:", None))
        self.label_75.setText(QCoreApplication.translate("Dialog", u"Planet min Pc", None))
        self.label_76.setText(QCoreApplication.translate("Dialog", u"Sun min Pc", None))
        self.label_77.setText(QCoreApplication.translate("Dialog", u"Ring min Pc", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"Contact Pressure:", None))
        self.label_73.setText(QCoreApplication.translate("Dialog", u"Planet min \u03c3b", None))
        self.label_72.setText(QCoreApplication.translate("Dialog", u"Sun min \u03c3b", None))
        self.label_74.setText(QCoreApplication.translate("Dialog", u"Ring min \u03c3b", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"Bending Stress:", None))
        self.label_163.setText(QCoreApplication.translate("Dialog", u"Actual Height", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.shape_page), QCoreApplication.translate("Dialog", u"Material and Height Requirements", None))
    # retranslateUi

