# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bldc-designer-2aSHFbg.ui'
##
## Created by: Qt User Interface Compiler version 5.15.16
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

try:
    from PySide2.QtCore import *  # type: ignore
    from PySide2.QtGui import *  # type: ignore
    from PySide2.QtWidgets import *  # type: ignore
except ImportError:
    from PySide.QtCore import *  # type: ignore
    from PySide.QtGui import *  # type: ignore
    from PySide.QtWidgets import *  # type: ignore

from .lock_button_ui import LockUnlockButton
from .torque_ui import QTorqueEdit
from .length_ui import QLengthEdit
from .fraction_ui import QFractionEdit
from .eval_ui import QEvalEdit
from .rotational_velocity_ui import QRotationalVelocityEdit
from .temperature_ui import QTemperatureEdit
from .voltage_ui import QVoltageEdit
from pyqtgraph import PlotWidget
from .inf_xy_grid import InfXYGridWidget


import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
class Ui_BLDCDialog(object):
    def setupUi(self, BLDCDialog):
        if not BLDCDialog.objectName():
            BLDCDialog.setObjectName(u"BLDCDialog")
        BLDCDialog.resize(1174, 748)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(BLDCDialog.sizePolicy().hasHeightForWidth())
        BLDCDialog.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(BLDCDialog)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(BLDCDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.stator_display_tab = QWidget()
        self.stator_display_tab.setObjectName(u"stator_display_tab")
        self.verticalLayout = QVBoxLayout(self.stator_display_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_2 = QWidget(self.stator_display_tab)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.display_axle_checkbox = QCheckBox(self.widget_2)
        self.display_axle_checkbox.setObjectName(u"display_axle_checkbox")

        self.horizontalLayout.addWidget(self.display_axle_checkbox)

        self.display_bearing_checkbox = QCheckBox(self.widget_2)
        self.display_bearing_checkbox.setObjectName(u"display_bearing_checkbox")

        self.horizontalLayout.addWidget(self.display_bearing_checkbox)

        self.display_stator_core_checkbox = QCheckBox(self.widget_2)
        self.display_stator_core_checkbox.setObjectName(u"display_stator_core_checkbox")

        self.horizontalLayout.addWidget(self.display_stator_core_checkbox)

        self.display_wires_checkbox = QCheckBox(self.widget_2)
        self.display_wires_checkbox.setObjectName(u"display_wires_checkbox")

        self.horizontalLayout.addWidget(self.display_wires_checkbox)

        self.display_magnets_checkbox = QCheckBox(self.widget_2)
        self.display_magnets_checkbox.setObjectName(u"display_magnets_checkbox")

        self.horizontalLayout.addWidget(self.display_magnets_checkbox)

        self.display_outrunner_checkbox = QCheckBox(self.widget_2)
        self.display_outrunner_checkbox.setObjectName(u"display_outrunner_checkbox")

        self.horizontalLayout.addWidget(self.display_outrunner_checkbox)

        self.display_height_checkbox = QCheckBox(self.widget_2)
        self.display_height_checkbox.setObjectName(u"display_height_checkbox")

        self.horizontalLayout.addWidget(self.display_height_checkbox)


        self.verticalLayout.addWidget(self.widget_2)

        self.stator_plot_widget = PlotWidget(self.stator_display_tab)
        self.stator_plot_widget.setObjectName(u"stator_plot_widget")

        self.verticalLayout.addWidget(self.stator_plot_widget)

        self.tabWidget.addTab(self.stator_display_tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_8 = QGroupBox(self.tab_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setMaximumSize(QSize(16777215, 80))
        self.gridLayout_8 = QGridLayout(self.groupBox_8)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.display_magnet_pitch_factor_radio_button = QRadioButton(self.groupBox_8)
        self.slot_pole_button_group = QButtonGroup(BLDCDialog)
        self.slot_pole_button_group.setObjectName(u"slot_pole_button_group")
        self.slot_pole_button_group.addButton(self.display_magnet_pitch_factor_radio_button)
        self.display_magnet_pitch_factor_radio_button.setObjectName(u"display_magnet_pitch_factor_radio_button")

        self.gridLayout_8.addWidget(self.display_magnet_pitch_factor_radio_button, 1, 2, 1, 1)

        self.display_chording_radio_button = QRadioButton(self.groupBox_8)
        self.slot_pole_button_group.addButton(self.display_chording_radio_button)
        self.display_chording_radio_button.setObjectName(u"display_chording_radio_button")

        self.gridLayout_8.addWidget(self.display_chording_radio_button, 1, 1, 1, 1)

        self.display_slot_pole_radio_button = QRadioButton(self.groupBox_8)
        self.slot_pole_button_group.addButton(self.display_slot_pole_radio_button)
        self.display_slot_pole_radio_button.setObjectName(u"display_slot_pole_radio_button")

        self.gridLayout_8.addWidget(self.display_slot_pole_radio_button, 1, 4, 1, 1)

        self.display_winding_distribution_radio_button = QRadioButton(self.groupBox_8)
        self.slot_pole_button_group.addButton(self.display_winding_distribution_radio_button)
        self.display_winding_distribution_radio_button.setObjectName(u"display_winding_distribution_radio_button")

        self.gridLayout_8.addWidget(self.display_winding_distribution_radio_button, 1, 3, 1, 1)

        self.display_coil_span_radio_button = QRadioButton(self.groupBox_8)
        self.slot_pole_button_group.addButton(self.display_coil_span_radio_button)
        self.display_coil_span_radio_button.setObjectName(u"display_coil_span_radio_button")

        self.gridLayout_8.addWidget(self.display_coil_span_radio_button, 1, 0, 1, 1)

        self.display_winding_factor_radio_button = QRadioButton(self.groupBox_8)
        self.slot_pole_button_group.addButton(self.display_winding_factor_radio_button)
        self.display_winding_factor_radio_button.setObjectName(u"display_winding_factor_radio_button")
        self.display_winding_factor_radio_button.setChecked(True)

        self.gridLayout_8.addWidget(self.display_winding_factor_radio_button, 0, 0, 1, 1)

        self.display_freq_at_rpm_radio_button = QRadioButton(self.groupBox_8)
        self.slot_pole_button_group.addButton(self.display_freq_at_rpm_radio_button)
        self.display_freq_at_rpm_radio_button.setObjectName(u"display_freq_at_rpm_radio_button")

        self.gridLayout_8.addWidget(self.display_freq_at_rpm_radio_button, 0, 1, 1, 1)

        self.display_cogging_freq_radio_button = QRadioButton(self.groupBox_8)
        self.slot_pole_button_group.addButton(self.display_cogging_freq_radio_button)
        self.display_cogging_freq_radio_button.setObjectName(u"display_cogging_freq_radio_button")

        self.gridLayout_8.addWidget(self.display_cogging_freq_radio_button, 0, 2, 1, 1)

        self.display_winding_balance_radio_button = QRadioButton(self.groupBox_8)
        self.slot_pole_button_group.addButton(self.display_winding_balance_radio_button)
        self.display_winding_balance_radio_button.setObjectName(u"display_winding_balance_radio_button")

        self.gridLayout_8.addWidget(self.display_winding_balance_radio_button, 0, 3, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.tab_2)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.remove_no_symmetry_checkbox = QCheckBox(self.groupBox_9)
        self.remove_no_symmetry_checkbox.setObjectName(u"remove_no_symmetry_checkbox")

        self.horizontalLayout_4.addWidget(self.remove_no_symmetry_checkbox)

        self.remove_unbalanced_checkbox = QCheckBox(self.groupBox_9)
        self.remove_unbalanced_checkbox.setObjectName(u"remove_unbalanced_checkbox")

        self.horizontalLayout_4.addWidget(self.remove_unbalanced_checkbox)

        self.remove_ns_is_nm_checkbox = QCheckBox(self.groupBox_9)
        self.remove_ns_is_nm_checkbox.setObjectName(u"remove_ns_is_nm_checkbox")

        self.horizontalLayout_4.addWidget(self.remove_ns_is_nm_checkbox)

        self.remove_q_less_0_25_checkbox = QCheckBox(self.groupBox_9)
        self.remove_q_less_0_25_checkbox.setObjectName(u"remove_q_less_0_25_checkbox")

        self.horizontalLayout_4.addWidget(self.remove_q_less_0_25_checkbox)

        self.remove_q_gt_0_5_checkbox = QCheckBox(self.groupBox_9)
        self.remove_q_gt_0_5_checkbox.setObjectName(u"remove_q_gt_0_5_checkbox")

        self.horizontalLayout_4.addWidget(self.remove_q_gt_0_5_checkbox)


        self.verticalLayout_2.addWidget(self.groupBox_9)

        self.slot_pole_grid_widget = InfXYGridWidget(self.tab_2)
        self.slot_pole_grid_widget.setObjectName(u"slot_pole_grid_widget")

        self.verticalLayout_2.addWidget(self.slot_pole_grid_widget)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_3 = QVBoxLayout(self.tab_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.graph_widget = QWidget(self.tab_5)
        self.graph_widget.setObjectName(u"graph_widget")

        self.verticalLayout_3.addWidget(self.graph_widget)

        self.tabWidget.addTab(self.tab_5, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.tabWidget_2 = QTabWidget(BLDCDialog)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setMaximumSize(QSize(400, 16777215))
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea = QScrollArea(self.tab_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -126, 362, 1151))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.default_settings_combobox = QComboBox(self.groupBox_3)
        self.default_settings_combobox.addItem("")
        self.default_settings_combobox.addItem("")
        self.default_settings_combobox.addItem("")
        self.default_settings_combobox.addItem("")
        self.default_settings_combobox.addItem("")
        self.default_settings_combobox.setObjectName(u"default_settings_combobox")

        self.gridLayout_2.addWidget(self.default_settings_combobox, 0, 0, 1, 1)

        self.default_settings_apply_button = QPushButton(self.groupBox_3)
        self.default_settings_apply_button.setObjectName(u"default_settings_apply_button")

        self.gridLayout_2.addWidget(self.default_settings_apply_button, 0, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.motor_torque_lock = LockUnlockButton(self.groupBox)
        self.motor_torque_lock.setObjectName(u"motor_torque_lock")

        self.gridLayout.addWidget(self.motor_torque_lock, 4, 2, 1, 1)

        self.max_volts_lock = LockUnlockButton(self.groupBox)
        self.max_volts_lock.setObjectName(u"max_volts_lock")

        self.gridLayout.addWidget(self.max_volts_lock, 5, 2, 1, 1)

        self.gearbox_ratio_lock = LockUnlockButton(self.groupBox)
        self.gearbox_ratio_lock.setObjectName(u"gearbox_ratio_lock")

        self.gridLayout.addWidget(self.gearbox_ratio_lock, 2, 2, 1, 1)

        self.gearbox_ratio_lineedit = QFractionEdit(self.groupBox)
        self.gearbox_ratio_lineedit.setObjectName(u"gearbox_ratio_lineedit")

        self.gridLayout.addWidget(self.gearbox_ratio_lineedit, 2, 1, 1, 1)

        self.max_volts_lineedit = QVoltageEdit(self.groupBox)
        self.max_volts_lineedit.setObjectName(u"max_volts_lineedit")

        self.gridLayout.addWidget(self.max_volts_lineedit, 5, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

        self.output_torque_lineedit = QTorqueEdit(self.groupBox)
        self.output_torque_lineedit.setObjectName(u"output_torque_lineedit")

        self.gridLayout.addWidget(self.output_torque_lineedit, 1, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.output_rpm_lineedit = QRotationalVelocityEdit(self.groupBox)
        self.output_rpm_lineedit.setObjectName(u"output_rpm_lineedit")

        self.gridLayout.addWidget(self.output_rpm_lineedit, 0, 1, 1, 1)

        self.output_torque_lock = LockUnlockButton(self.groupBox)
        self.output_torque_lock.setObjectName(u"output_torque_lock")

        self.gridLayout.addWidget(self.output_torque_lock, 1, 2, 1, 1)

        self.output_rpm_lock = LockUnlockButton(self.groupBox)
        self.output_rpm_lock.setObjectName(u"output_rpm_lock")

        self.gridLayout.addWidget(self.output_rpm_lock, 0, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.motor_rpm_lineedit = QRotationalVelocityEdit(self.groupBox)
        self.motor_rpm_lineedit.setObjectName(u"motor_rpm_lineedit")

        self.gridLayout.addWidget(self.motor_rpm_lineedit, 3, 1, 1, 1)

        self.motor_rpm_lock = LockUnlockButton(self.groupBox)
        self.motor_rpm_lock.setObjectName(u"motor_rpm_lock")

        self.gridLayout.addWidget(self.motor_rpm_lock, 3, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.motor_torque_lineedit = QTorqueEdit(self.groupBox)
        self.motor_torque_lineedit.setObjectName(u"motor_torque_lineedit")

        self.gridLayout.addWidget(self.motor_torque_lineedit, 4, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)

        self.max_temp_lineedit = QTemperatureEdit(self.groupBox)
        self.max_temp_lineedit.setObjectName(u"max_temp_lineedit")

        self.gridLayout.addWidget(self.max_temp_lineedit, 6, 1, 1, 1)

        self.max_temp_lock = LockUnlockButton(self.groupBox)
        self.max_temp_lock.setObjectName(u"max_temp_lock")

        self.gridLayout.addWidget(self.max_temp_lock, 6, 2, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)

        self.radius_lineedit = QLengthEdit(self.groupBox_2)
        self.radius_lineedit.setObjectName(u"radius_lineedit")

        self.gridLayout_3.addWidget(self.radius_lineedit, 0, 1, 1, 1)

        self.radius_lock = LockUnlockButton(self.groupBox_2)
        self.radius_lock.setObjectName(u"radius_lock")

        self.gridLayout_3.addWidget(self.radius_lock, 0, 2, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)

        self.num_slots_lineedit = QEvalEdit(self.groupBox_2)
        self.num_slots_lineedit.setObjectName(u"num_slots_lineedit")

        self.gridLayout_3.addWidget(self.num_slots_lineedit, 1, 1, 1, 1)

        self.num_slots_lock = LockUnlockButton(self.groupBox_2)
        self.num_slots_lock.setObjectName(u"num_slots_lock")

        self.gridLayout_3.addWidget(self.num_slots_lock, 1, 2, 1, 1)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 2, 0, 1, 1)

        self.num_magnets_lineedit = QEvalEdit(self.groupBox_2)
        self.num_magnets_lineedit.setObjectName(u"num_magnets_lineedit")

        self.gridLayout_3.addWidget(self.num_magnets_lineedit, 2, 1, 1, 1)

        self.num_magnets_lock = LockUnlockButton(self.groupBox_2)
        self.num_magnets_lock.setObjectName(u"num_magnets_lock")

        self.gridLayout_3.addWidget(self.num_magnets_lock, 2, 2, 1, 1)

        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_3.addWidget(self.label_11, 3, 0, 1, 1)

        self.air_gap_lineedit = QLengthEdit(self.groupBox_2)
        self.air_gap_lineedit.setObjectName(u"air_gap_lineedit")

        self.gridLayout_3.addWidget(self.air_gap_lineedit, 3, 1, 1, 1)

        self.air_gap_lock = LockUnlockButton(self.groupBox_2)
        self.air_gap_lock.setObjectName(u"air_gap_lock")

        self.gridLayout_3.addWidget(self.air_gap_lock, 3, 2, 1, 1)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_3.addWidget(self.label_12, 4, 0, 1, 1)

        self.axle_radius_lineedit = QLengthEdit(self.groupBox_2)
        self.axle_radius_lineedit.setObjectName(u"axle_radius_lineedit")

        self.gridLayout_3.addWidget(self.axle_radius_lineedit, 4, 1, 1, 1)

        self.axle_radius_lock = LockUnlockButton(self.groupBox_2)
        self.axle_radius_lock.setObjectName(u"axle_radius_lock")

        self.gridLayout_3.addWidget(self.axle_radius_lock, 4, 2, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.stator_inner_radius_lock = LockUnlockButton(self.groupBox_4)
        self.stator_inner_radius_lock.setObjectName(u"stator_inner_radius_lock")

        self.gridLayout_4.addWidget(self.stator_inner_radius_lock, 8, 4, 1, 1)

        self.label_16 = QLabel(self.groupBox_4)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_4.addWidget(self.label_16, 8, 0, 1, 1)

        self.stator_inner_radius_lineedit = QLengthEdit(self.groupBox_4)
        self.stator_inner_radius_lineedit.setObjectName(u"stator_inner_radius_lineedit")

        self.gridLayout_4.addWidget(self.stator_inner_radius_lineedit, 8, 2, 1, 1)

        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_4.addWidget(self.label_13, 0, 0, 1, 2)

        self.hammerhead_length_lock = LockUnlockButton(self.groupBox_4)
        self.hammerhead_length_lock.setObjectName(u"hammerhead_length_lock")

        self.gridLayout_4.addWidget(self.hammerhead_length_lock, 7, 4, 1, 1)

        self.hammerhead_length_lineedit = QLengthEdit(self.groupBox_4)
        self.hammerhead_length_lineedit.setObjectName(u"hammerhead_length_lineedit")

        self.gridLayout_4.addWidget(self.hammerhead_length_lineedit, 7, 2, 1, 1)

        self.slot_width_lineedit = QLengthEdit(self.groupBox_4)
        self.slot_width_lineedit.setObjectName(u"slot_width_lineedit")

        self.gridLayout_4.addWidget(self.slot_width_lineedit, 0, 2, 1, 2)

        self.label_15 = QLabel(self.groupBox_4)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_4.addWidget(self.label_15, 7, 0, 1, 1)

        self.hammerhead_width_lineedit = QLengthEdit(self.groupBox_4)
        self.hammerhead_width_lineedit.setObjectName(u"hammerhead_width_lineedit")

        self.gridLayout_4.addWidget(self.hammerhead_width_lineedit, 1, 2, 1, 1)

        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_4.addWidget(self.label_14, 1, 0, 1, 1)

        self.slot_width_lock = LockUnlockButton(self.groupBox_4)
        self.slot_width_lock.setObjectName(u"slot_width_lock")

        self.gridLayout_4.addWidget(self.slot_width_lock, 0, 4, 1, 1)

        self.hammerhead_width_lock = LockUnlockButton(self.groupBox_4)
        self.hammerhead_width_lock.setObjectName(u"hammerhead_width_lock")

        self.gridLayout_4.addWidget(self.hammerhead_width_lock, 1, 4, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_5 = QGridLayout(self.groupBox_5)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.magnet_thickness_lock = LockUnlockButton(self.groupBox_5)
        self.magnet_thickness_lock.setObjectName(u"magnet_thickness_lock")

        self.gridLayout_5.addWidget(self.magnet_thickness_lock, 0, 2, 1, 1)

        self.magnet_thickness_lineedit = QLengthEdit(self.groupBox_5)
        self.magnet_thickness_lineedit.setObjectName(u"magnet_thickness_lineedit")

        self.gridLayout_5.addWidget(self.magnet_thickness_lineedit, 0, 1, 1, 1)

        self.label_17 = QLabel(self.groupBox_5)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_5.addWidget(self.label_17, 0, 0, 1, 1)

        self.label_18 = QLabel(self.groupBox_5)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_5.addWidget(self.label_18, 1, 0, 1, 1)

        self.outrunner_thickness_lock = LockUnlockButton(self.groupBox_5)
        self.outrunner_thickness_lock.setObjectName(u"outrunner_thickness_lock")

        self.gridLayout_5.addWidget(self.outrunner_thickness_lock, 1, 2, 1, 1)

        self.outrunner_thickness_lineedit = QLengthEdit(self.groupBox_5)
        self.outrunner_thickness_lineedit.setObjectName(u"outrunner_thickness_lineedit")

        self.gridLayout_5.addWidget(self.outrunner_thickness_lineedit, 1, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_6 = QGridLayout(self.groupBox_6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.turns_per_slot_lineedit = QEvalEdit(self.groupBox_6)
        self.turns_per_slot_lineedit.setObjectName(u"turns_per_slot_lineedit")

        self.gridLayout_6.addWidget(self.turns_per_slot_lineedit, 2, 1, 1, 1)

        self.wire_diameter_lineedit = QLengthEdit(self.groupBox_6)
        self.wire_diameter_lineedit.setObjectName(u"wire_diameter_lineedit")

        self.gridLayout_6.addWidget(self.wire_diameter_lineedit, 0, 1, 1, 1)

        self.label_21 = QLabel(self.groupBox_6)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_6.addWidget(self.label_21, 3, 0, 1, 1)

        self.needle_diameter_lock = LockUnlockButton(self.groupBox_6)
        self.needle_diameter_lock.setObjectName(u"needle_diameter_lock")

        self.gridLayout_6.addWidget(self.needle_diameter_lock, 3, 2, 1, 1)

        self.needle_diameter_lineedit = QLengthEdit(self.groupBox_6)
        self.needle_diameter_lineedit.setObjectName(u"needle_diameter_lineedit")

        self.gridLayout_6.addWidget(self.needle_diameter_lineedit, 3, 1, 1, 1)

        self.label_19 = QLabel(self.groupBox_6)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_6.addWidget(self.label_19, 0, 0, 1, 1)

        self.wire_diameter_lock = LockUnlockButton(self.groupBox_6)
        self.wire_diameter_lock.setObjectName(u"wire_diameter_lock")

        self.gridLayout_6.addWidget(self.wire_diameter_lock, 0, 2, 1, 1)

        self.turns_per_layer_lineedit = QLineEdit(self.groupBox_6)
        self.turns_per_layer_lineedit.setObjectName(u"turns_per_layer_lineedit")

        self.gridLayout_6.addWidget(self.turns_per_layer_lineedit, 4, 1, 1, 1)

        self.label_22 = QLabel(self.groupBox_6)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_6.addWidget(self.label_22, 4, 0, 1, 1)

        self.turns_per_slot_lock = LockUnlockButton(self.groupBox_6)
        self.turns_per_slot_lock.setObjectName(u"turns_per_slot_lock")

        self.gridLayout_6.addWidget(self.turns_per_slot_lock, 2, 2, 1, 1)

        self.tight_pack_checkbox = QCheckBox(self.groupBox_6)
        self.tight_pack_checkbox.setObjectName(u"tight_pack_checkbox")

        self.gridLayout_6.addWidget(self.tight_pack_checkbox, 5, 1, 1, 1)

        self.label_20 = QLabel(self.groupBox_6)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_6.addWidget(self.label_20, 2, 0, 1, 1)

        self.turns_per_layer_lock = LockUnlockButton(self.groupBox_6)
        self.turns_per_layer_lock.setObjectName(u"turns_per_layer_lock")

        self.gridLayout_6.addWidget(self.turns_per_layer_lock, 4, 2, 1, 1)

        self.needle_winding_checkbox = QCheckBox(self.groupBox_6)
        self.needle_winding_checkbox.setObjectName(u"needle_winding_checkbox")

        self.gridLayout_6.addWidget(self.needle_winding_checkbox, 6, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_6)

        self.groupBox_7 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_7 = QGridLayout(self.groupBox_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.drill_bit_diameter_lineedit = QLengthEdit(self.groupBox_7)
        self.drill_bit_diameter_lineedit.setObjectName(u"drill_bit_diameter_lineedit")

        self.gridLayout_7.addWidget(self.drill_bit_diameter_lineedit, 1, 1, 1, 1)

        self.drill_bit_diameter_lock = LockUnlockButton(self.groupBox_7)
        self.drill_bit_diameter_lock.setObjectName(u"drill_bit_diameter_lock")

        self.gridLayout_7.addWidget(self.drill_bit_diameter_lock, 1, 2, 1, 1)

        self.label_23 = QLabel(self.groupBox_7)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_7.addWidget(self.label_23, 1, 0, 1, 1)

        self.cnc_milling_checkbox = QCheckBox(self.groupBox_7)
        self.cnc_milling_checkbox.setObjectName(u"cnc_milling_checkbox")

        self.gridLayout_7.addWidget(self.cnc_milling_checkbox, 0, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_7)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget_2.addTab(self.tab_4, "")

        self.horizontalLayout_2.addWidget(self.tabWidget_2)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)

        self.retranslateUi(BLDCDialog)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(BLDCDialog)
    # setupUi

    def retranslateUi(self, BLDCDialog):
        BLDCDialog.setWindowTitle(QCoreApplication.translate("BLDCDialog", u"Dialog", None))
        self.display_axle_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Axle", None))
        self.display_bearing_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Bearing", None))
        self.display_stator_core_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Stator Core", None))
        self.display_wires_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Wires", None))
        self.display_magnets_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Magnets", None))
        self.display_outrunner_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Outrunner", None))
        self.display_height_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Height", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stator_display_tab), QCoreApplication.translate("BLDCDialog", u"Stator", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("BLDCDialog", u"Display", None))
        self.display_magnet_pitch_factor_radio_button.setText(QCoreApplication.translate("BLDCDialog", u"Magnet Pitch Factor", None))
        self.display_chording_radio_button.setText(QCoreApplication.translate("BLDCDialog", u"Chording", None))
        self.display_slot_pole_radio_button.setText(QCoreApplication.translate("BLDCDialog", u"slot/pole", None))
        self.display_winding_distribution_radio_button.setText(QCoreApplication.translate("BLDCDialog", u"winding distribution", None))
        self.display_coil_span_radio_button.setText(QCoreApplication.translate("BLDCDialog", u"Coil Span Factor", None))
        self.display_winding_factor_radio_button.setText(QCoreApplication.translate("BLDCDialog", u"Winding Factor", None))
        self.display_freq_at_rpm_radio_button.setText(QCoreApplication.translate("BLDCDialog", u"Freq@Motor RPM", None))
        self.display_cogging_freq_radio_button.setText(QCoreApplication.translate("BLDCDialog", u"CoggingFreq", None))
        self.display_winding_balance_radio_button.setText(QCoreApplication.translate("BLDCDialog", u"Winding Balance", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("BLDCDialog", u"Remove Invalid", None))
        self.remove_no_symmetry_checkbox.setText(QCoreApplication.translate("BLDCDialog", u" No Symmetry (GCD=1)", None))
        self.remove_unbalanced_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Unbalanced", None))
        self.remove_ns_is_nm_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Ns=Nm", None))
        self.remove_q_less_0_25_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Slot-Pole Ratio<0.25", None))
        self.remove_q_gt_0_5_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Slot-Pole Ratio>0.5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("BLDCDialog", u"Slot-Pole", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("BLDCDialog", u"Graphs", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("BLDCDialog", u"Default Settings", None))
        self.default_settings_combobox.setItemText(0, QCoreApplication.translate("BLDCDialog", u"Quadcopter Motor", None))
        self.default_settings_combobox.setItemText(1, QCoreApplication.translate("BLDCDialog", u"Micro Motor", None))
        self.default_settings_combobox.setItemText(2, QCoreApplication.translate("BLDCDialog", u"MEMS Motor", None))
        self.default_settings_combobox.setItemText(3, QCoreApplication.translate("BLDCDialog", u"Car Motor", None))
        self.default_settings_combobox.setItemText(4, QCoreApplication.translate("BLDCDialog", u"Airplane Motor", None))

        self.default_settings_apply_button.setText(QCoreApplication.translate("BLDCDialog", u"Apply", None))
        self.groupBox.setTitle(QCoreApplication.translate("BLDCDialog", u"Input/Output Properties", None))
        self.label_3.setText(QCoreApplication.translate("BLDCDialog", u"Gearbox Ratio", None))
        self.label_4.setText(QCoreApplication.translate("BLDCDialog", u"Motor Torque", None))
        self.label_5.setText(QCoreApplication.translate("BLDCDialog", u"Motor RPM", None))
        self.label_6.setText(QCoreApplication.translate("BLDCDialog", u"Max Volts", None))
        self.label_2.setText(QCoreApplication.translate("BLDCDialog", u"Output Torque", None))
        self.label.setText(QCoreApplication.translate("BLDCDialog", u"Output RPM", None))
        self.label_7.setText(QCoreApplication.translate("BLDCDialog", u"Max Temp", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("BLDCDialog", u"Physical Properties", None))
        self.label_8.setText(QCoreApplication.translate("BLDCDialog", u"Radius", None))
        self.label_9.setText(QCoreApplication.translate("BLDCDialog", u"Num Slots", None))
        self.label_10.setText(QCoreApplication.translate("BLDCDialog", u"Num Magnets", None))
        self.label_11.setText(QCoreApplication.translate("BLDCDialog", u"Air Gap", None))
        self.label_12.setText(QCoreApplication.translate("BLDCDialog", u"Axle Radius", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("BLDCDialog", u"Stator", None))
        self.label_16.setText(QCoreApplication.translate("BLDCDialog", u"Stator Inner Radius", None))
        self.label_13.setText(QCoreApplication.translate("BLDCDialog", u"Slot Width", None))
        self.label_15.setText(QCoreApplication.translate("BLDCDialog", u"Hammerhead Length", None))
        self.label_14.setText(QCoreApplication.translate("BLDCDialog", u"Hammerhead Width", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("BLDCDialog", u"Magnet and Outrunner", None))
        self.label_17.setText(QCoreApplication.translate("BLDCDialog", u"Magnet Thickness", None))
        self.label_18.setText(QCoreApplication.translate("BLDCDialog", u"Outrunner Thickness", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("BLDCDialog", u"Wire", None))
        self.label_21.setText(QCoreApplication.translate("BLDCDialog", u"Needle Diameter", None))
        self.label_19.setText(QCoreApplication.translate("BLDCDialog", u"Wire Diameter", None))
        self.label_22.setText(QCoreApplication.translate("BLDCDialog", u"Turns Per Layer", None))
        self.tight_pack_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Tight Pack (Hexagonal)", None))
        self.label_20.setText(QCoreApplication.translate("BLDCDialog", u"Turns Per Slot", None))
        self.needle_winding_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"Needle Winding", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("BLDCDialog", u"CNC", None))
        self.label_23.setText(QCoreApplication.translate("BLDCDialog", u"Drill Bit Diameter", None))
        self.cnc_milling_checkbox.setText(QCoreApplication.translate("BLDCDialog", u"CNC Milling", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("BLDCDialog", u"Tab 1", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("BLDCDialog", u"Tab 2", None))
    # retranslateUi

