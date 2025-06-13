from dataclasses import dataclass, asdict
import numpy as np
from typing import List, Any, TYPE_CHECKING
import json
if TYPE_CHECKING:
    from main_window import BLDCWindow
else:
    from typing import Any
    BLDCWindow = Any
try:
    from PySide2.QtWidgets import QFileDialog
except ImportError:
    from PySide.QtWidgets import QFileDialog

@dataclass
class StatorParameters:
    num_slots: int
    slot_width: float  # in mm
    hammerhead_width: float  # in mm
    hammerhead_length: float  # in mm
    stator_inner_radius: float  # in mm
    air_gap: float  # in mm
    cnc_milling: bool
    drill_bit_diameter: float  # in mm
    magnet_inner_radius: float  # in mm
    height:float
    dist_from_base:float

    @property
    def slot_width_half(self) -> float:
        return self.slot_width / 2

    @property
    def drill_bit_radius(self) -> float:
        return self.drill_bit_diameter / 2 if self.cnc_milling else 0

    @property
    def r_outer(self) -> float:
        return self.magnet_inner_radius - self.air_gap - self.hammerhead_length

@dataclass
class MagnetParameters:
    radius: float  # Outer radius of the motor in mm
    outrunner_thickness: float  # in mm
    magnet_type: str  # "square" or "arc"
    num_magnets: int
    magnet_thickness: float  # in mm
    magnet_width: float  # in mm for square, in degrees for arc
    magnet_height: float
    square_magnet_rounded_corners: bool = False  # Only for square magnets
    square_magnet_rounding_radius: float = 0.0  # in mm, only for square magnets

    @property
    def magnet_outer_radius(self) -> float:
        return self.radius - self.outrunner_thickness

    @property
    def dist_from_wall(self) -> float:
        if self.magnet_type == "square":
            effective_width = self.magnet_width
            if self.square_magnet_rounded_corners:
                effective_width -= 2 * self.square_magnet_rounding_radius
            return self.magnet_outer_radius - self.magnet_outer_radius * np.sin(
                np.arccos(effective_width / 2 / self.magnet_outer_radius)
            )
        return 0.0

    @property
    def magnet_inner_radius(self) -> float:
        return self.magnet_outer_radius - self.magnet_thickness - self.dist_from_wall

    @property
    def max_magnet_width(self) -> float:
        if self.magnet_type == "square":
            theta = (self.num_magnets - 2) * np.pi / (2 * self.num_magnets)
            h = self.magnet_outer_radius * np.sin(theta) - (self.magnet_thickness - self.square_magnet_rounding_radius)
            return 2 * h * np.cos(theta)
        else:
            return 360.0 / self.num_magnets

    @property
    def dist_from_each_other(self) -> float:
        if self.magnet_type == "square":
            return self.max_magnet_width - self.magnet_width
        else:
            return 2 * self.magnet_inner_radius * np.sin(np.deg2rad(self.max_magnet_width - self.magnet_width) / 2)

@dataclass
class AxleParameters:
    axle_radius: float  # in mm
    below_base_len: float
    above_outrunner_len: float

@dataclass
class OutrunnerParameters:
    radius: float  # Outer radius of the motor in mm
    outrunner_thickness: float  # in mm
    height: float
    height_gap: float

    @property
    def inner_radius(self) -> float:
        return self.radius - self.outrunner_thickness

@dataclass
class WireParameters:
    wire_diameter: float  # in mm
    num_turns_per_slot: int
    tight_pack: bool
    needle_winding: bool
    needle_diameter: float  # in mm
    turns_list: List[List[int]]  # List of lists representing turns per layer

@dataclass
class BLDCParameters:
    stator: StatorParameters
    magnet: MagnetParameters
    axle: AxleParameters
    outrunner: OutrunnerParameters
    wire: WireParameters
    base_height:float

def serialize(bldc_window: BLDCWindow) -> BLDCParameters:
    """Serialize a BLDCWindow instance into a BLDCParameters instance."""
    magnet_type = "square" if bldc_window.ui.magnet_tab_widget.currentIndex() == 0 else "arc"
    num_magnets = (
        bldc_window.ui.num_square_magnets_lineedit.get_value()
        if magnet_type == "square"
        else bldc_window.ui.num_arc_magnets_lineedit.get_value()
    )
    magnet_thickness = (
        bldc_window.ui.square_magnet_thickness_lineedit.get_mm_value()
        if magnet_type == "square"
        else bldc_window.ui.arc_magnet_thickness_lineedit.get_mm_value()
    )
    magnet_width = (
        bldc_window.ui.square_magnet_width_lineedit.get_mm_value()
        if magnet_type == "square"
        else bldc_window.ui.arc_magnet_width_lineedit.get_degrees_value()
    )
    magnet_height = (
        bldc_window.ui.square_magnet_height_lineedit.get_mm_value()
        if magnet_type == "square"
        else bldc_window.ui.arc_magnet_width_lineedit.get_degrees_value()
    )

    # Compute magnet_inner_radius using the logic from get_magnet_inner_radius
    radius = bldc_window.ui.radius_lineedit.get_mm_value()
    outrunner_thickness = bldc_window.ui.outrunner_thickness_lineedit.get_mm_value()
    magnet_outer_radius = radius - outrunner_thickness
    if magnet_type == "square":
        effective_width = magnet_width
        if bldc_window.ui.square_magnet_rounded_corners.isChecked():
            rad = bldc_window.ui.square_magnet_rounding_radius_lineedit.get_mm_value()
            effective_width -= 2 * rad
        dist_from_wall = magnet_outer_radius - magnet_outer_radius * np.sin(
            np.arccos(effective_width / 2 / magnet_outer_radius)
        )
        magnet_inner_radius = magnet_outer_radius - magnet_thickness - dist_from_wall
    else:
        magnet_inner_radius = magnet_outer_radius - magnet_thickness

    try:
        turns_list = eval(bldc_window.ui.turns_per_layer_lineedit.text())
    except Exception:
        turns_list = [[]]  # Default empty list if parsing fails

    return BLDCParameters(
        stator=StatorParameters(
            num_slots=int(bldc_window.ui.num_slots_lineedit.get_value()),
            slot_width=bldc_window.ui.slot_width_lineedit.get_mm_value(),
            hammerhead_width=bldc_window.ui.hammerhead_width_lineedit.get_mm_value(),
            hammerhead_length=bldc_window.ui.hammerhead_length_lineedit.get_mm_value(),
            stator_inner_radius=bldc_window.ui.stator_inner_radius_lineedit.get_mm_value(),
            air_gap=bldc_window.ui.air_gap_lineedit.get_mm_value(),
            cnc_milling=bldc_window.ui.cnc_milling_checkbox.isChecked(),
            drill_bit_diameter=bldc_window.ui.drill_bit_diameter_lineedit.get_mm_value(),
            magnet_inner_radius=magnet_inner_radius,
            height=bldc_window.ui.stator_height_lineedit.get_mm_value(),
            dist_from_base=bldc_window.ui.stator_dist_from_base_lineedit.get_mm_value()
        ),
        magnet=MagnetParameters(
            radius=radius,
            outrunner_thickness=outrunner_thickness,
            magnet_type=magnet_type,
            num_magnets=num_magnets,
            magnet_thickness=magnet_thickness,
            magnet_width=magnet_width,
            magnet_height=magnet_height,
            square_magnet_rounded_corners=bldc_window.ui.square_magnet_rounded_corners.isChecked() if magnet_type == "square" else False,
            square_magnet_rounding_radius=bldc_window.ui.square_magnet_rounding_radius_lineedit.get_mm_value() if magnet_type == "square" else 0.0
        ),
        axle=AxleParameters(
            axle_radius=bldc_window.ui.axle_radius_lineedit.get_mm_value(),
            below_base_len=bldc_window.ui.axle_below_base_height_lineedit.get_mm_value(),
            above_outrunner_len=bldc_window.ui.axle_above_outrunner_height_lineedit.get_mm_value()
        ),
        outrunner=OutrunnerParameters(
            radius=radius,
            outrunner_thickness=outrunner_thickness,
            height=bldc_window.ui.outrunner_height_lineedit.get_mm_value(),
            height_gap=bldc_window.ui.outrunner_height_gap_lineedit.get_mm_value()
        ),
        wire=WireParameters(
            wire_diameter=bldc_window.ui.wire_diameter_lineedit.get_mm_value(),
            num_turns_per_slot=int(bldc_window.ui.turns_per_slot_lineedit.get_value()),
            tight_pack=bldc_window.ui.tight_pack_checkbox.isChecked(),
            needle_winding=bldc_window.ui.needle_winding_checkbox.isChecked(),
            needle_diameter=bldc_window.ui.needle_diameter_lineedit.get_mm_value(),
            turns_list=turns_list
        ),
        base_height=bldc_window.ui.base_height_lineedit.get_mm_value()
    )

def save_to_file(bldc_window: BLDCWindow, file_path: str) -> None:
    """Save BLDCParameters to a JSON file."""
    params = serialize(bldc_window)
    with open(file_path, 'w') as f:
        json.dump(asdict(params), f, indent=4)

def load_from_file(file_path: str) -> BLDCParameters:
    """Load BLDCParameters from a JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return BLDCParameters(
        stator=StatorParameters(**data['stator']),
        magnet=MagnetParameters(**data['magnet']),
        axle=AxleParameters(**data['axle']),
        outrunner=OutrunnerParameters(**data['outrunner']),
        wire=WireParameters(**data['wire']),
        base_height=data['base_height']
    )

def create_bldc_window() -> Any:
    """Create a new BLDCWindow instance."""
    from main_window import BLDCWindow  # Import here to avoid circular imports
    return BLDCWindow()

def deserialize(bldc_window: BLDCWindow, params: BLDCParameters) -> None:
    """Set the parameters of an existing BLDCWindow instance from a BLDCParameters instance."""
    # Set stator parameters
    bldc_window.ui.num_slots_lineedit.set_value(params.stator.num_slots)
    bldc_window.ui.slot_width_lineedit.set_mm_value(params.stator.slot_width)
    bldc_window.ui.hammerhead_width_lineedit.set_mm_value(params.stator.hammerhead_width)
    bldc_window.ui.hammerhead_length_lineedit.set_mm_value(params.stator.hammerhead_length)
    bldc_window.ui.stator_inner_radius_lineedit.set_mm_value(params.stator.stator_inner_radius)
    bldc_window.ui.air_gap_lineedit.set_mm_value(params.stator.air_gap)
    bldc_window.ui.cnc_milling_checkbox.setChecked(params.stator.cnc_milling)
    bldc_window.ui.drill_bit_diameter_lineedit.set_mm_value(params.stator.drill_bit_diameter)
    bldc_window.ui.stator_height_lineedit.set_mm_value(params.stator.height)
    bldc_window.ui.stator_dist_from_base_lineedit.set_mm_value(params.stator.dist_from_base)

    # Set magnet parameters
    bldc_window.ui.radius_lineedit.set_mm_value(params.magnet.radius)
    bldc_window.ui.outrunner_thickness_lineedit.set_mm_value(params.magnet.outrunner_thickness)
    bldc_window.ui.magnet_tab_widget.setCurrentIndex(0 if params.magnet.magnet_type == "square" else 1)
    if params.magnet.magnet_type == "square":  #todo: remove grok's lazy assumption that we don't want to keep more data
        bldc_window.ui.num_square_magnets_lineedit.set_value(params.magnet.num_magnets)
        bldc_window.ui.square_magnet_thickness_lineedit.set_mm_value(params.magnet.magnet_thickness)
        bldc_window.ui.square_magnet_width_lineedit.set_mm_value(params.magnet.magnet_width)
        bldc_window.ui.square_magnet_rounded_corners.setChecked(params.magnet.square_magnet_rounded_corners)
        bldc_window.ui.square_magnet_rounding_radius_lineedit.set_mm_value(params.magnet.square_magnet_rounding_radius)
        bldc_window.ui.square_magnet_height_lineedit.set_mm_value(params.magnet.magnet_height)
    else:
        bldc_window.ui.num_arc_magnets_lineedit.set_value(params.magnet.num_magnets)
        bldc_window.ui.arc_magnet_thickness_lineedit.set_mm_value(params.magnet.magnet_thickness)
        bldc_window.ui.arc_magnet_width_lineedit.set_degrees_value(params.magnet.magnet_width)
        bldc_window.ui.arc_magnet_height_lineedit.set_mm_value(params.magnet.magnet_height)

    # Set axle parameters
    bldc_window.ui.axle_radius_lineedit.set_mm_value(params.axle.axle_radius)
    bldc_window.ui.axle_below_base_height_lineedit.set_mm_value(params.axle.below_base_len)
    bldc_window.ui.axle_above_outrunner_height_lineedit.set_mm_value(params.axle.above_outrunner_len)

    # Set outrunner parameters (shared with magnet)
    bldc_window.ui.radius_lineedit.set_mm_value(params.outrunner.radius)
    bldc_window.ui.outrunner_thickness_lineedit.set_mm_value(params.outrunner.outrunner_thickness)
    bldc_window.ui.outrunner_height_lineedit.set_mm_value(params.outrunner.height)
    bldc_window.ui.outrunner_height_gap_lineedit.set_mm_value(params.outrunner.height_gap)

    # Set wire parameters
    bldc_window.ui.wire_diameter_lineedit.set_mm_value(params.wire.wire_diameter)
    bldc_window.ui.turns_per_slot_lineedit.set_value(params.wire.num_turns_per_slot)
    bldc_window.ui.tight_pack_checkbox.setChecked(params.wire.tight_pack)
    bldc_window.ui.needle_winding_checkbox.setChecked(params.wire.needle_winding)
    bldc_window.ui.needle_diameter_lineedit.set_mm_value(params.wire.needle_diameter)
    bldc_window.ui.turns_per_layer_lineedit.setText(str(params.wire.turns_list))

    bldc_window.ui.base_height_lineedit.set_mm_value(params.base_height)

def on_save_button_clicked(bldc_window: BLDCWindow) -> None:
    """Handle the Save button click event."""
    file_path, _ = QFileDialog.getSaveFileName(
        bldc_window,
        "Save BLDC Parameters",
        "",
        "JSON Files (*.json);;All Files (*)"
    )
    if file_path:
        save_to_file(bldc_window, file_path)

def on_open_button_clicked(bldc_window: BLDCWindow) -> None:
    """Handle the Open button click event."""
    file_path, _ = QFileDialog.getOpenFileName(
        bldc_window,
        "Open BLDC Parameters",
        "",
        "JSON Files (*.json);;All Files (*)"
    )
    if file_path:
        params = load_from_file(file_path)
        deserialize(bldc_window, params)
        bldc_window.update_visualization(bldc_window)

def connect_serialization_buttons(bldc_window: BLDCWindow):
    bldc_window.ui.settings_save_button.clicked.connect(lambda: on_save_button_clicked(bldc_window))
    bldc_window.ui.settings_load_button.clicked.connect(lambda: on_open_button_clicked(bldc_window))