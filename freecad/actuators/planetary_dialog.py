import math

from .compiled_ui.planetary_ui import Ui_Dialog
try:
    from PySide2.QtCore import *  # type: ignore
    from PySide2.QtGui import *  # type: ignore
    from PySide2.QtWidgets import *  # type: ignore
except ImportError:
    from PySide.QtCore import *  # type: ignore
    from PySide.QtGui import *  # type: ignore
    from PySide.QtWidgets import *  # type: ignore
from .search_planetaries import PlanetarySearchWorker, GearboxResult

import math as m


def form_factor(num_teeth, pressure_angle_degrees):
    return 0.4461457824814488+(math.sin((-10.057793276492692+pressure_angle_degrees)/180*math.pi))*math.log1p(0.0497526912165741*num_teeth)

class PlanetaryDesign:
    def __init__(
        self,
        fixed: str,
        _input: str,
        output: str,
        inv_gear_ratio,
        planet_teeth: int,
        sun_teeth: int,
        ring_teeth: int,
        num_planets: int,
        input_torque: float,
        beta: float,
        is_double_helix: bool,
        pressure_angle: float,
        module: float,
        height: float,
        material: str,
    ):
        self.fixed = fixed
        self._input = _input
        self.output = output
        self.inv_gear_ratio = inv_gear_ratio
        self.planet_teeth = planet_teeth
        self.sun_teeth = sun_teeth
        self.ring_teeth = ring_teeth
        self.num_planets = num_planets
        self.input_torque = input_torque
        self.beta = beta
        self.is_double_helix = is_double_helix
        self.pressure_angle = pressure_angle
        self.module = module
        self.height = height
        self.material = material

    def __repr__(self):
        return (
            f"PlanetaryDesign(fixed={self.fixed}, input={self._input}, output={self.output}, "
            f"inv_gear_ratio={self.inv_gear_ratio}, planet_teeth={self.planet_teeth}, "
            f"sun_teeth={self.sun_teeth}, ring_teeth={self.ring_teeth}, num_planets={self.num_planets}, "
            f"input_torque={self.input_torque}, beta={self.beta}, is_double_helix={self.is_double_helix}, "
            f"pressure_angle={self.pressure_angle}, module={self.module}, height={self.height}, "
            f"material={self.material})"
        )

class PlanetaryDialog(QDialog):
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

        self.ui.max_in_torque_lineedit.textChanged.connect(self.recalculate_torque)

        self.ui.poisson_ratio_lineedit.textChanged.connect(self.recalculate_stress)
        self.ui.elastic_modulus_lineedit.textChanged.connect(self.recalculate_stress)
        self.ui.sun_ft_lineedit.textChanged.connect(self.recalculate_stress)
        self.ui.sun_form_factor_lineedit.textChanged.connect(self.recalculate_stress)
        self.ui.planet_ft_lineedit.textChanged.connect(self.recalculate_stress)
        self.ui.planet_form_factor_lineedit.textChanged.connect(self.recalculate_stress)
        self.ui.ring_ft_lineedit.textChanged.connect(self.recalculate_stress)
        self.ui.ring_form_factor_lineedit.textChanged.connect(self.recalculate_stress)

        self.ui.min_num_of_planets_spinbox.valueChanged.connect(self.on_min_num_of_planets_spinbox_changed)
        self.ui.max_num_of_planets_spinbox.valueChanged.connect(self.on_max_num_of_planets_spinbox_changed)
        self.ui.num_results_spinbox.valueChanged.connect(self.on_num_results_spinbox_changed)
        self.ui.gear_ratio_options_combobox.currentIndexChanged.connect(self.gear_ratio_options_combobox_changed)

        self.ui.actual_diameter_lineedit.textChanged.connect(self.on_actual_diameter_user_changed)
        self.ui.actual_module_lineedit.textChanged.connect(self.on_actual_module_user_changed)
        self.ui.actual_module_slider.valueChanged.connect(self.on_actual_module_slider_user_changed)
        self.ui.actual_height_lineedit.textChanged.connect(self.on_actual_height_user_changed)
        self.ui.actual_height_slider.valueChanged.connect(self.on_actual_height_slider_user_changed)

        self.ui.beta_lineedit.textChanged.connect(self.on_beta_lineedit_changed)
        self.ui.pressure_angle_lineedit.textChanged.connect(self.recalculate_torque)

    def finish_return(self):
        planetary = self.ui.gear_ratio_options_combobox.get_selected_object()
        input_torque = self.ui.max_in_torque_lineedit.get_nm_value()
        beta = self.ui.beta_lineedit.get_degrees_value()
        is_double_helix = self.ui.double_helix_checkbox.isChecked()
        pressure_angle = self.ui.pressure_angle_lineedit.get_degrees_value()
        module = self.ui.actual_module_lineedit.get_mm_value()
        height = self.ui.actual_height_lineedit.get_mm_value()
        material = self.ui.material_combobox.currentText()

        planetary_design = PlanetaryDesign(
            planetary.fixed,  # str
            planetary._input,  # str
            planetary.output,  # str
            planetary.inv_gear_ratio,  # Fraction
            planetary.planet_teeth,  # int
            planetary.sun_teeth,  # int
            planetary.ring_teeth,  # int
            planetary.num_planets,  # int
            input_torque,  # float
            beta,
            is_double_helix,
            pressure_angle,
            module,
            height,
            material  # str or object
        )
        return planetary_design

    def on_pressure_angle_lineedit_changed(self, _):
        self.recalculate_torque(_)
        self.recalculate_stress(_)

    def on_beta_lineedit_changed(self, _):
        self.recalculate_torque(_)
        self.recalculate_stress(_)

    def on_actual_diameter_user_changed(self, _):
        if not self.computing:
            planetary = self.ui.gear_ratio_options_combobox.get_selected_object()
            if self.ui.actual_diameter_lineedit.get_mm_value()!=0.0 and planetary is not None:
                self.computing = True
                try:
                    self.ui.actual_module_lineedit.set_mm_value(self.ui.actual_diameter_lineedit.get_mm_value()/(planetary.ring_teeth + 6))
                    self.ui.actual_module_slider.setFractionalValue(self.ui.actual_module_lineedit.get_mm_value())
                finally:
                    self.computing = False
            self.ui.actual_module_lineedit_lock.is_locked = True
        self.recalculate_torque(_)
        self.recalculate_stress(_)

    def on_actual_module_user_changed(self, _):
        if not self.computing:
            planetary = self.ui.gear_ratio_options_combobox.get_selected_object()
            if self.ui.actual_module_lineedit.get_mm_value()!=0.0 and planetary is not None:
                self.computing = True
                try:
                    self.ui.actual_diameter_lineedit.set_mm_value(self.ui.actual_module_lineedit.get_mm_value()*(planetary.ring_teeth + 6))
                    self.ui.actual_module_slider.setFractionalValue(self.ui.actual_module_lineedit.get_mm_value())
                finally:
                    self.computing = False
            self.ui.actual_module_lineedit_lock.is_locked = True
        self.recalculate_torque(_)
        self.recalculate_stress(_)

    def on_actual_module_slider_user_changed(self, _):
        if not self.computing:
            planetary = self.ui.gear_ratio_options_combobox.get_selected_object()
            if self.ui.actual_module_slider.value()!=0.0 and planetary is not None:
                self.computing = True
                try:
                    self.ui.actual_module_lineedit.set_mm_value(self.ui.actual_module_slider.getFractionalValue())
                    self.ui.actual_diameter_lineedit.set_mm_value(self.ui.actual_module_slider.getFractionalValue()*(planetary.ring_teeth + 6))
                finally:
                    self.computing = False
            self.ui.actual_module_lineedit_lock.is_locked = True
        self.recalculate_torque(_)
        self.recalculate_stress(_)

    def on_actual_height_user_changed(self, _):
        if not self.computing:
            if self.ui.actual_height_lineedit.get_mm_value()!=0.0:
                self.computing = True
                try:
                    self.ui.actual_height_slider.setFractionalValue(self.ui.actual_height_lineedit.get_mm_value())
                finally:
                    self.computing = False
            self.ui.actual_height_lineedit_lock.is_locked = True
        self.recalculate_stress(_)

    def on_actual_height_slider_user_changed(self, _):
        if not self.computing:
            if self.ui.actual_height_slider.value()!=0.0:
                self.computing = True
                try:
                    self.ui.actual_height_lineedit.set_mm_value(self.ui.actual_height_slider.getFractionalValue())
                finally:
                    self.computing = False
            self.ui.actual_height_lineedit_lock.is_locked = True
        self.recalculate_stress(_)

    def recalculate_max_module_display(self):
        planetary = self.ui.gear_ratio_options_combobox.get_selected_object()
        if planetary is None:
            return
        ring_diameter = self.ui.max_ring_diam_lineedit.get_mm_value()

        module = ring_diameter / (planetary.ring_teeth+6)
        self.ui.max_module_display_lineedit.set_mm_value(module)
        self.ui.actual_module_slider.setFractionalMaximum(module)
        self.ui.actual_module_slider.setFractionalSingleStep((module - self.ui.actual_module_slider.getFractionalMinimum())/100)

    def recalculate_min_ring_diam_display(self):
        planetary = self.ui.gear_ratio_options_combobox.get_selected_object()
        if planetary is None:
            return
        module = self.ui.min_module_lineedit.get_mm_value()

        ring_diameter = module*(planetary.ring_teeth + 6)
        self.ui.min_diameter_display_lineedit.set_mm_value(ring_diameter)

    def gear_ratio_options_combobox_changed(self, _):
        if not self.computing:
            self.ui.gear_ratio_options_combobox_lock.is_locked = True
        self.recalculate_max_module_display()
        self.recalculate_min_ring_diam_display()
        self.recalculate_torque(_)
        self.recalculate_stress(_)

    def on_num_results_spinbox_changed(self, _):
        if not self.computing:
            self.ui.num_results_spinbox_lock.is_locked = True

    def on_min_num_of_planets_spinbox_changed(self, _):
        if not self.computing:
            self.ui.min_num_of_planets_spinbox_lock.is_locked = True

    def on_max_num_of_planets_spinbox_changed(self, _):
        if not self.computing:
            self.ui.max_num_of_planets_spinbox_lock.is_locked = True

    def recalculate_torque(self, _):
        planetary = self.ui.gear_ratio_options_combobox.get_selected_object()
        if not isinstance(planetary, GearboxResult):
            return  # todo: set them all back to 0 or blank
        in_torque = self.ui.max_in_torque_lineedit.get_nm_value()
        if in_torque==0:
            return
        beta = self.ui.beta_lineedit.get_degrees_value()
        pressure_angle = self.ui.pressure_angle_lineedit.get_degrees_value()
        if pressure_angle==0:
            return
        is_double_helix = self.ui.double_helix_checkbox.isChecked()
        module = self.ui.actual_module_lineedit.get_mm_value()
        if module==0:
            return

        if planetary._input=="Sun":
            self.ui.sun_t_lineedit.set_nm_value(in_torque)
            if planetary.output=="Ring":
                self.ui.ring_t_lineedit.set_nm_value(in_torque/planetary.inv_gear_ratio)
                self.ui.carrier_t_lineedit.set_nm_value(0)
            elif planetary.output=="Carrier":
                self.ui.carrier_t_lineedit.set_nm_value(in_torque/planetary.inv_gear_ratio)
                self.ui.ring_t_lineedit.set_nm_value(0)
        elif planetary._input=="Ring":
            self.ui.ring_t_lineedit.set_nm_value(in_torque)
            if planetary.output=="Sun":
                self.ui.sun_t_lineedit.set_nm_value(in_torque/planetary.inv_gear_ratio)
                self.ui.carrier_t_lineedit.set_nm_value(0)
            elif planetary.output=="Carrier":
                self.ui.carrier_t_lineedit.set_nm_value(in_torque / planetary.inv_gear_ratio)
                self.ui.sun_t_lineedit.set_nm_value(0)
        elif planetary._input=="Carrier":
            self.ui.carrier_t_lineedit.set_nm_value(in_torque)
            if planetary.output=="Sun":
                self.ui.sun_t_lineedit.set_nm_value(in_torque / planetary.inv_gear_ratio)
                self.ui.ring_t_lineedit.set_nm_value(0)
            elif planetary.output=="Ring":
                self.ui.ring_t_lineedit.set_nm_value(in_torque / planetary.inv_gear_ratio)
                self.ui.sun_t_lineedit.set_nm_value(0)

        self.ui.planet_t_lineedit.set_nm_value(
            self.ui.sun_t_lineedit.get_nm_value()*(planetary.planet_teeth/planetary.sun_teeth)-
            self.ui.ring_t_lineedit.get_nm_value() * (planetary.planet_teeth / planetary.ring_teeth)
        )

        self.ui.load_sharing_planets_lineedit.setText(str(planetary.num_planets))

        ring_pitch_circle_diameter = module * planetary.ring_teeth
        sun_pitch_circle_diameter = module * planetary.sun_teeth
        planet_pitch_circle_diameter = module * planetary.planet_teeth
        carrier_pitch_circle_diameter = sun_pitch_circle_diameter + planet_pitch_circle_diameter

        sun_t = self.ui.sun_t_lineedit.get_nm_value()
        sun_ft = (2*sun_t/(sun_pitch_circle_diameter/1000))/planetary.num_planets
        sun_fr = sun_ft * math.tan(pressure_angle/180*math.pi)
        sun_fa = sun_ft * math.tan(beta/180*math.pi)
        sun_fn = math.sqrt(sun_ft**2 + sun_fr**2 + sun_fa**2)
        self.ui.sun_ft_lineedit.set_n_value(sun_ft)
        self.ui.sun_fr_lineedit.set_n_value(sun_fr)
        self.ui.sun_fa_lineedit.set_n_value(sun_fa)
        self.ui.sun_fn_lineedit.set_n_value(sun_fn)

        planet_t = self.ui.planet_t_lineedit.get_nm_value()
        planet_ft = (2 * planet_t / (planet_pitch_circle_diameter / 1000)) / planetary.num_planets
        planet_fr = planet_ft * math.tan(pressure_angle / 180 * math.pi)
        planet_fa = planet_ft * math.tan(beta / 180 * math.pi)
        planet_fn = math.sqrt(planet_ft ** 2 + planet_fr ** 2 + planet_fa ** 2)
        self.ui.planet_ft_lineedit.set_n_value(planet_ft)
        self.ui.planet_fr_lineedit.set_n_value(planet_fr)
        self.ui.planet_fa_lineedit.set_n_value(planet_fa)
        self.ui.planet_fn_lineedit.set_n_value(planet_fn)

        ring_t = self.ui.ring_t_lineedit.get_nm_value()
        ring_ft = (2 * ring_t / (ring_pitch_circle_diameter / 1000)) / planetary.num_planets
        ring_fr = ring_ft * math.tan(pressure_angle / 180 * math.pi)
        ring_fa = ring_ft * math.tan(beta / 180 * math.pi)
        ring_fn = math.sqrt(ring_ft ** 2 + ring_fr ** 2 + ring_fa ** 2)
        self.ui.ring_ft_lineedit.set_n_value(ring_ft)
        self.ui.ring_fr_lineedit.set_n_value(ring_fr)
        self.ui.ring_fa_lineedit.set_n_value(ring_fa)
        self.ui.ring_fn_lineedit.set_n_value(ring_fn)

        carrier_t = self.ui.carrier_t_lineedit.get_nm_value()
        carrier_ft = (2 * carrier_t / (carrier_pitch_circle_diameter / 1000)) / planetary.num_planets
        carrier_fr = carrier_ft * math.tan(pressure_angle / 180 * math.pi)
        carrier_fn = math.sqrt(carrier_ft ** 2 + carrier_fr ** 2)
        self.ui.carrier_ft_lineedit.set_n_value(carrier_ft)
        self.ui.carrier_fr_lineedit.set_n_value(carrier_fr)
        self.ui.carrier_fn_lineedit.set_n_value(carrier_fn)

        sun_teeth_virtual = planetary.sun_teeth/(math.cos(beta/180*math.pi)**3)
        planet_teeth_virtual = planetary.planet_teeth/(math.cos(beta/180*math.pi)**3)
        ring_teeth_virtual = planetary.ring_teeth/(math.cos(beta/180*math.pi)**3)
        self.ui.sun_zy_lineedit.set_value(sun_teeth_virtual)
        self.ui.planet_zy_lineedit.set_value(planet_teeth_virtual)
        self.ui.ring_zy_lineedit.set_value(ring_teeth_virtual)

        sun_form_factor = form_factor(sun_teeth_virtual, pressure_angle)
        planet_form_factor = form_factor(planet_teeth_virtual, pressure_angle)
        ring_form_factor = form_factor(ring_teeth_virtual, pressure_angle)
        self.ui.sun_form_factor_lineedit.set_value(sun_form_factor)
        self.ui.planet_form_factor_lineedit.set_value(planet_form_factor)
        self.ui.ring_form_factor_lineedit.set_value(ring_form_factor)

    def recalculate_stress(self, _):
        planetary = self.ui.gear_ratio_options_combobox.get_selected_object()
        if not isinstance(planetary, GearboxResult):
            return  # todo: set them all back to 0 or blank
        beta = self.ui.beta_lineedit.get_degrees_value()
        module = self.ui.actual_module_lineedit.get_mm_value()
        if module == 0:
            return
        pressure_angle = self.ui.pressure_angle_lineedit.get_degrees_value()
        if pressure_angle == 0:
            return
        poisson_ratio = self.ui.poisson_ratio_lineedit.get_value()
        elastic_modulus = self.ui.elastic_modulus_lineedit.get_pa_value()
        if elastic_modulus==0:
            return

        sun_tangential_load = self.ui.sun_ft_lineedit.get_n_value()
        sun_form_factor = self.ui.sun_form_factor_lineedit.get_value()
        height = self.ui.actual_height_lineedit.get_mm_value()
        planet_tangential_load = self.ui.planet_ft_lineedit.get_n_value()
        planet_form_factor = self.ui.planet_form_factor_lineedit.get_value()
        ring_tangential_load = self.ui.ring_ft_lineedit.get_n_value()
        ring_form_factor = self.ui.ring_form_factor_lineedit.get_value()

        fwe = height/math.cos(beta/180*math.pi)  # https://www.khkgears.us/media/1225/the-benefits-of-converting-to-helical-gearing.pdf
        # fwe should include contact ratio, probably

        # https://www.engineersedge.com/gears/lewis-factor.htm
        sun_bend_stress = sun_tangential_load / (module/1000 * fwe/1000 * sun_form_factor)
        self.ui.sun_bend_stress_lineedit.set_pa_value(sun_bend_stress)


        planet_bend_stress = planet_tangential_load / (module/1000 * fwe/1000 * planet_form_factor)
        self.ui.planet_bend_stress_lineedit.set_pa_value(planet_bend_stress)


        ring_bend_stress = ring_tangential_load / (module/1000 * fwe/1000 * ring_form_factor)
        self.ui.ring_bend_stress_lineedit.set_pa_value(ring_bend_stress)

        # https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=fe1a219b86058a5cf569d4222cff595df1794eed
        material_factor = math.sqrt(1/((1-poisson_ratio**2)/elastic_modulus))
        tooth_shape_factor = math.sqrt(1/(math.sin(pressure_angle/180*math.pi)))

        sun_contact_pressure = math.sqrt(
            sun_tangential_load*(1+planetary.sun_teeth/planetary.planet_teeth)/
            ((module/1000)*planetary.sun_teeth*(fwe/1000)*math.pi)
        ) * material_factor * tooth_shape_factor
        self.ui.sun_contact_pressure.set_pa_value(sun_contact_pressure)

        # I could do max of planet_teeth/sun_teeth and planet_teeth/ring_teeth,
        # but that's always going to be planet_teeth/sun_teeth
        planet_contact_pressure = math.sqrt(
            planet_tangential_load * (1 + (planetary.planet_teeth / planetary.sun_teeth)) /
            ((module / 1000) * planetary.planet_teeth * (fwe / 1000) * math.pi)
        ) * material_factor * tooth_shape_factor
        self.ui.planet_contact_pressure.set_pa_value(planet_contact_pressure)

        ring_contact_pressure = math.sqrt(
            ring_tangential_load * (1 + planetary.ring_teeth / planetary.sun_teeth) /
            ((module / 1000) * planetary.planet_teeth * (fwe / 1000) * math.pi)
        ) * material_factor * tooth_shape_factor
        self.ui.ring_contact_pressure.set_pa_value(ring_contact_pressure)

        max_reported_bend = max(ring_bend_stress, planet_bend_stress, sun_bend_stress)
        max_reported_fatigue = max(ring_contact_pressure, planet_contact_pressure, sun_contact_pressure)

        max_bend_stress = self.ui.max_bend_stress_lineedit.get_pa_value()
        if max_bend_stress==0:
            return
        max_fatigue_stress = self.ui.max_fatigue_stress_lineedit.get_pa_value()
        if max_fatigue_stress==0:
            return

        bend_safety = max_bend_stress/max_reported_bend
        fatigue_safety = max_fatigue_stress/max_reported_fatigue

        self.ui.bend_safety_factor_lineedit.setText(f"{bend_safety*100:.1f}%")
        self.ui.contact_safety_factor_lineedit.setText(f"{fatigue_safety*100:.1f}%")

        if bend_safety<1:
            self.ui.bend_safety_factor_lineedit.setStyleSheet("background-color: red;")
            self.ui.bend_safety_factor_lineedit.setToolTip("Gear teeth will permanently deform or snap")
        elif bend_safety<1.5:
            self.ui.bend_safety_factor_lineedit.setStyleSheet("background-color: yellow;")
            self.ui.bend_safety_factor_lineedit.setToolTip("Gear teeth may permanently deform or snap")
        else:
            self.ui.bend_safety_factor_lineedit.setStyleSheet("")
            self.ui.bend_safety_factor_lineedit.setToolTip("")

        if fatigue_safety<1:
            self.ui.contact_safety_factor_lineedit.setStyleSheet("background-color: red;")
            self.ui.contact_safety_factor_lineedit.setToolTip("Gear teeth will pit")
        elif fatigue_safety < 1.5:
            self.ui.contact_safety_factor_lineedit.setStyleSheet("background-color: yellow;")
            self.ui.contact_safety_factor_lineedit.setToolTip("Gear teeth may pit")
        else:
            self.ui.contact_safety_factor_lineedit.setStyleSheet("")
            self.ui.contact_safety_factor_lineedit.setToolTip("")

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
            self.ui.min_ring_teeth_spinbox.value(),
            self.ui.max_ring_teeth_spinbox.value(),
            self.ui.target_inverse_gear_ratio_lineedit.get_value(),
            self.ui.gear_addendum_lineedit.get_mm_value(),
            self.ui.planet_clearance_lineedit.get_mm_value(),
            self.ui.num_results_spinbox.value(),
            self.ui.min_num_of_planets_spinbox.value(),
            self.ui.max_num_of_planets_spinbox.value(),
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
        self.ui.min_height_display_lineedit.set_mm_value(self.ui.min_module_lineedit.get_mm_value())
        self.recalculate_min_ring_diam_display()

    def on_min_module_user_changed(self, _):
        if not self.computing:
            if self.ui.min_module_lineedit.get_mm_value()!=0.0:
                self.computing = True
                try:
                    self.ui.min_circular_pitch_lineedit.set_mm_value(self.ui.min_module_lineedit.get_mm_value()*m.pi)
                finally:
                    self.computing = False
            self.ui.min_module_lineedit_lock.is_locked = True
        self.ui.min_module_display_lineedit.set_mm_value(self.ui.min_module_lineedit.get_mm_value())
        self.ui.actual_module_slider.setFractionalMinimum(self.ui.min_module_lineedit.get_mm_value())
        self.ui.actual_module_slider.setFractionalSingleStep((self.ui.actual_module_slider.getFractionalMaximum() - self.ui.min_module_lineedit.get_mm_value())/100)
        self.recalculate_min_ring_diam_display()

    def on_min_circular_pitch_user_changed(self, _):
        if not self.computing:
            if self.ui.min_circular_pitch_lineedit.get_mm_value()!=0.0:
                self.computing = True
                try:
                    self.ui.min_module_lineedit.set_mm_value(self.ui.min_circular_pitch_lineedit.get_mm_value()/m.pi)
                    self.ui.min_module_display_lineedit.set_mm_value(self.ui.min_circular_pitch_lineedit.get_mm_value()/m.pi)
                    self.ui.actual_module_slider.setFractionalMinimum(self.ui.min_module_lineedit.get_mm_value())
                    self.ui.actual_module_slider.setFractionalSingleStep(
                        (self.ui.actual_module_slider.getFractionalMaximum() - self.ui.min_module_lineedit.get_mm_value()) / 100)
                finally:
                    self.computing = False
            self.ui.min_module_lineedit_lock.is_locked = True

    def on_max_ring_diam_lock_changed(self, _):
        if not self.ui.max_ring_teeth_spinbox_lock.is_locked:
            self.recalculate_max_ring()
        self.ui.max_diameter_display_lineedit.set_mm_value(self.ui.max_ring_diam_lineedit.get_mm_value())
        self.recalculate_max_module_display()

    def on_max_ring_diam_user_changed(self, _):
        if not self.computing:
            self.ui.max_ring_diam_lineedit_lock.is_locked = True
        self.ui.max_diameter_display_lineedit.set_mm_value(self.ui.max_ring_diam_lineedit.get_mm_value())
        self.recalculate_max_module_display()

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
                    self.ui.max_height_display_lineedit.set_mm_value(self.ui.min_height_lineedit.get_mm_value())
                    self.ui.actual_height_slider.setFractionalMaximum(self.ui.max_height_display_lineedit.get_mm_value())
                    self.ui.actual_height_slider.setFractionalSingleStep((self.ui.max_height_display_lineedit.get_mm_value() - self.ui.min_height_display_lineedit.get_mm_value()) / 100)
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
                    self.ui.min_height_display_lineedit.set_mm_value(self.ui.max_height_lineedit.get_mm_value())
                    self.ui.actual_height_slider.setFractionalMinimum(self.ui.min_height_display_lineedit.get_mm_value())
                    self.ui.actual_height_slider.setFractionalSingleStep((
                                                                           self.ui.max_height_display_lineedit.get_mm_value() - self.ui.min_height_display_lineedit.get_mm_value()) / 100)
                    self.ui.min_height_lineedit.setToolTip("")
                    self.ui.min_height_lineedit.setStyleSheet("")
                finally:
                    self.computing = False
        else:
            self.ui.min_height_lineedit.setToolTip("")
            self.ui.min_height_lineedit.setStyleSheet("")

    def on_min_height_user_changed(self, _):
        self.ui.min_height_display_lineedit.set_mm_value(self.ui.min_height_lineedit.get_mm_value())
        if not self.computing:
            self.ui.min_height_lineedit_lock.is_locked = True
        self.ui.actual_height_slider.setFractionalMinimum(self.ui.min_height_display_lineedit.get_mm_value())
        self.ui.actual_height_slider.setFractionalSingleStep((
                                                           self.ui.max_height_display_lineedit.get_mm_value() - self.ui.min_height_display_lineedit.get_mm_value()) / 100)

    def on_max_height_user_changed(self, _):
        self.ui.max_height_display_lineedit.set_mm_value(self.ui.max_height_lineedit.get_mm_value())
        if not self.computing:
            self.ui.max_height_lineedit_lock.is_locked = True
        self.ui.actual_height_slider.setFractionalMaximum(self.ui.max_height_display_lineedit.get_mm_value())
        self.ui.actual_height_slider.setFractionalSingleStep((self.ui.max_height_display_lineedit.get_mm_value() - self.ui.min_height_display_lineedit.get_mm_value()) / 100)

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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = PlanetaryDialog()
    dialog.show()
    sys.exit(app.exec_())
