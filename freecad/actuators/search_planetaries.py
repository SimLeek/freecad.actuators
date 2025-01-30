from rtree import index
from fractions import Fraction
import math
from itertools import permutations


class GearboxConstraint:
    """
    A class to encapsulate gearbox constraints and provide methods to evaluate
    and search for gear ratios matching given criteria.
    """

    def __init__(
            self,
            min_planet_1_teeth,
            max_planet_1_teeth,
            min_sun_1_teeth,
            max_sun_1_teeth,
            num_planets=3,
            addendum=1,
            clearance=0.5,
            circular_pitch=4,
    ):
        """
        Initializes the GearboxConstraint with the given constraints.

        Args:
            min_planet_1_teeth (int): Minimum number of teeth for first stage planetary gears.
            max_planet_1_teeth (int): Maximum number of teeth for first stage planetary gears.
            min_sun_1_teeth (int): Minimum number of teeth for first stage sun gears.
            max_sun_1_teeth (int): Maximum number of teeth for first stage sun gears.
            num_planets (int): Number of planets in the system.
            addendum (float): Addendum circle diameter.
            clearance (float): Clearance between gears.
            circular_pitch (float): Circular pitch of the gears.
        """
        self.min_p1 = min_planet_1_teeth
        self.max_p1 = max_planet_1_teeth
        self.min_s1 = min_sun_1_teeth
        self.max_s1 = max_sun_1_teeth
        self.num_planets = num_planets
        self.addendum = addendum
        self.clearance = clearance
        self.circular_pitch = circular_pitch


class GearboxResult:
    """A class to encapsulate the results of a gearbox configuration."""

    def __init__(self, fixed, _input, output, inv_gear_ratio,
                 planet_teeth, sun_teeth, num_planets):
        """
        Initialize a GearboxResult instance.

        Args:
            inv_gear_ratio (Fraction): Calculated inverse gear ratio.
            planet_teeth (int): Teeth count for first stage planetary gears.
            sun_teeth (int): Teeth count for first stage sun gears.
        """
        self.fixed = fixed
        self._input = _input
        self.output = output
        self.inv_gear_ratio = inv_gear_ratio
        self.planet_teeth = planet_teeth
        self.sun_teeth = sun_teeth
        self.ring_teeth = 2*planet_teeth+sun_teeth
        self.num_planets = num_planets

    def __repr__(self):
        """
        String representation of the GearboxResult instance.
        Returns:
            str: Formatted string showing all component teeth counts and result.
        """
        return (f"["
                f"R⁻¹={self.inv_gear_ratio},"
                f" F={self.fixed},"
                f" I={self._input},"
                f" O={self.output},"
                f" S={self.sun_teeth},"
                f" P={self.planet_teeth},"
                f" R={self.planet_teeth}"
                f" Np={self.num_planets}"
                f"]")

    def tooltip(self):
        return (f"Inverse gear ratio={self.inv_gear_ratio}\n"
                f"Fixed={self.fixed}\n"
                f"Input={self._input}\n"
                f"Output={self.output}\n"
                f"Sun Teeth={self.sun_teeth}\n"
                f"Planet Teeth={self.planet_teeth}\n"
                f"Ring Teeth={self.planet_teeth}\n"
                f"Num Planets={self.num_planets}")

def evaluate_inverse_gear_ratio(planet_teeth: int, sun_teeth: int, fixed: str, input_: str, output: str) -> Fraction:
    """
    Calculates the gear ratio for a planetary gearbox given the fixed, input, and output selections.

    :param planet_teeth: Number of teeth on the planet gear.
    :param sun_teeth: Number of teeth on the sun gear.
    :param fixed: The fixed component ("Sun", "Ring", or "Carrier").
    :param input_: The input component ("Sun", "Ring", or "Carrier").
    :param output: The output component ("Sun", "Ring", or "Carrier").
    :return: The gear ratio (output speed / input speed).
    :raises ValueError: If the input is invalid or undefined.
    """

    ring_teeth = sun_teeth + 2 * planet_teeth  # Fundamental planetary equation

    # Define cases based on fixed component
    if fixed == "Sun":
        if input_ == "Ring" and output == "Carrier":
            return Fraction(ring_teeth, sun_teeth) + 1
        elif input_ == "Carrier" and output == "Ring":
            return Fraction(ring_teeth, (sun_teeth + ring_teeth))

    elif fixed == "Ring":
        if input_ == "Sun" and output == "Carrier":
            return Fraction(sun_teeth, (ring_teeth + sun_teeth))
        elif input_ == "Carrier" and output == "Sun":
            return 1 + Fraction(ring_teeth, sun_teeth)

    elif fixed == "Carrier":
        if input_ == "Sun" and output == "Ring":
            return Fraction(-sun_teeth , ring_teeth)  # Negative indicates direction reversal
        elif input_ == "Ring" and output == "Sun":
            return Fraction(-ring_teeth,sun_teeth)  # Negative indicates direction reversal

    raise ValueError(f"Invalid or undefined configuration: Fixed={fixed}, Input={input_}, Output={output}")


def evaluate_all_possible_ratios(planet_teeth: int, sun_teeth: int, fixed: str, input_: str, output: str):
    """
    Expands 'Any' values into all possible valid configurations and evaluates the gear ratios.

    :param planet_teeth: Number of teeth on the planet gear.
    :param sun_teeth: Number of teeth on the sun gear.
    :param fixed: The fixed component ("Sun", "Ring", "Carrier", "Any").
    :param input_: The input component ("Sun", "Ring", "Carrier", "Any").
    :param output: The output component ("Sun", "Ring", "Carrier", "Any").
    :return: A dictionary of valid configurations with their computed gear ratios.
    """

    possible_values = ["Sun", "Ring", "Carrier"]

    # Identify which elements are 'Any'
    any_slots = [slot for slot in [fixed, input_, output] if slot == "Any"]
    known_slots = [slot for slot in [fixed, input_, output] if slot != "Any"]

    # If one slot is Any, fill it with the remaining valid option
    if len(any_slots) == 1:
        remaining = list(set(possible_values) - set(known_slots))
        slot_combinations = [(remaining[0] if fixed == "Any" else fixed,
                              remaining[1] if input_ == "Any" else input_,
                              remaining[2] if output == "Any" else output)]

    # If two slots are Any, generate all valid permutations
    elif len(any_slots) == 2:
        slot_pos = [fixed, input_, output].index(known_slots[0])
        remaining_options = list(set(possible_values) - set(known_slots))
        slot_combinations = [[remaining_options[i],
                                    remaining_options[1 - i]]
                             for i in range(2)]
        for s in slot_combinations:
            s.insert(slot_pos, known_slots[0])

    # If all three are Any, generate all permutations
    elif len(any_slots) == 3:
        slot_combinations = list(permutations(possible_values, 3))

    else:
        # No 'Any' values, just evaluate the given configuration
        slot_combinations = [(fixed, input_, output)]

    results = {}
    for fixed_val, input_val, output_val in slot_combinations:
        try:
            ratio = evaluate_inverse_gear_ratio(planet_teeth, sun_teeth, fixed_val, input_val, output_val)
            results[(fixed_val, input_val, output_val)] = ratio
        except ValueError as e:
            results[(fixed_val, input_val, output_val)] = str(e)  # Store the error as a message

    return results


def ring_teeth(sun_teeth, planet_teeth):
    return 2*planet_teeth+sun_teeth
def _is_homogeneity_distribution_constraint_satisfied(sun_teeth, planet_teeth, num_planets):
    n = Fraction(ring_teeth(sun_teeth, planet_teeth)+sun_teeth, num_planets)
    return n%1==0

def _is_neighbor_constraint_satisfied(sun_teeth, planet_teeth, num_planets, addendum, clearance, circular_pitch):
    n = (sun_teeth+planet_teeth) * math.sin(2*math.pi/num_planets) - planet_teeth - 2 * addendum/circular_pitch - clearance/circular_pitch
    return n>0


def _find_closest_matches(idx, target_value, num_results=1):
    nearest_items_it = idx.nearest((target_value, 0, target_value, 0), num_results=num_results, objects=True)
    nearest_items_list = [n.object for n in nearest_items_it]
    nearest_items_list.sort(key=lambda x: abs(x.inv_gear_ratio - target_value))
    return nearest_items_list


def evaluate_and_search_2d(constraints, target_gear_ratio, update_progress=None, num_results=1, use_abs=False,
                           fixed='Any', input='Any', output='Any'):
    """
    Evaluates gearbox configurations based on given constraints and searches for the closest match to the target gear ratio.

    Args:
        constraints (GearboxConstraint): Gearbox constraint settings.
        target_gear_ratio (Fraction): Desired gear ratio.
        update_progress (callable, optional): Function to update progress.
        num_results (int, optional): Number of closest results to return.
        use_abs (bool, optional): Whether to use absolute values for comparisons.
        fixed (str, optional): Fixed gear designation.
        input (str, optional): Input gear designation.
        output (str, optional): Output gear designation.

    Returns:
        list[GearboxResult]: List of closest matching gearbox configurations.
    """
    p = index.Property()
    idx = index.Index(properties=p)

    full = (constraints.max_p1 + 1 - constraints.min_p1) * (constraints.max_s1 + 1 - constraints.min_s1)
    for planet_teeth in range(constraints.min_p1, constraints.max_p1 + 1):
        for sun_teeth in range(constraints.min_s1, constraints.max_s1 + 1):
            partial = ((planet_teeth - constraints.min_p1) * (constraints.max_s1 + 1 - constraints.min_s1) +
                       (sun_teeth - constraints.min_s1))
            if update_progress:
                update_progress((partial / full) * 100.0)

            is_homo = _is_homogeneity_distribution_constraint_satisfied(sun_teeth, planet_teeth,
                                                                      constraints.num_planets)
            is_good_neighbor = _is_neighbor_constraint_satisfied(sun_teeth, planet_teeth, constraints.num_planets,
                                                      constraints.addendum, constraints.clearance,
                                                      constraints.circular_pitch)

            if not ( is_homo and is_good_neighbor):
                continue

            result = evaluate_all_possible_ratios(planet_teeth, sun_teeth, fixed, input, output)
            for r_gear, r_val in result.items():
                if isinstance(r_val, str):
                    raise RuntimeError(r_val)
                abs_res = abs(r_val) if use_abs else r_val
                gearbox_result = GearboxResult(*r_gear, r_val, planet_teeth, sun_teeth, constraints.num_planets)
                idx.insert(0, (abs_res, 0, abs_res, 0), obj=gearbox_result)

    return _find_closest_matches(idx, target_gear_ratio, num_results)


if __name__ == "__main__":
    min_sun_1_teeth, max_sun_1_teeth = 6, 12
    min_planet_1_teeth, max_planet_1_teeth = 6, 24

    target_gear_ratio = 1/8
    import time
    t0 = time.time()
    # ring 2 is the output, so 2 is the secondary
    # the list is: [result, planet_2_teeth, sun_2_teeth, planet_1_teeth, sun_1_teeth]
    # so the last two items are the first gearbox
    module = 1.5
    circular_pitch = module*math.pi
    closest_match = evaluate_and_search_2d(min_planet_1_teeth, max_planet_1_teeth,
                                           min_sun_1_teeth, max_sun_1_teeth,
                                           target_gear_ratio, update_progress = None, num_results=10, use_abs=True,
                                           clearance=0.5, # mm
                                           num_planets=3, circular_pitch=circular_pitch, fixed='Any', input='Sun')  # use 3 for higher gear ratios but lower stability. 4 can get some good precision
    # idk why, but addendum=18 stops the planet gears from being too big.

    t1 = time.time()
    for m in closest_match:
        print(f"match: {m}")
    print(f"time:{t1-t0}")

from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QProgressBar
from PySide2.QtCore import QThread, Signal
from fractions import Fraction
import time  # Simulating long function

# Placeholder for long-running function

class PlanetarySearchWorker(QThread):
    """Worker thread for running long_func without freezing UI."""
    progress_updated = Signal(int)
    finished = Signal(list)  # Emits the result list when done

    def __init__(self, min_planet_teeth, max_planet_teeth, min_sun_teeth, max_sun_teeth, target_gear_ratio, gear_addendum, planet_clearance, num_results, num_planets, circular_pitch, use_abs, fixed, input, output):
        super().__init__()

        self.constraints = GearboxConstraint(
                min_planet_teeth,
                max_planet_teeth,
                min_sun_teeth,
                max_sun_teeth,
                num_planets=num_planets,
                addendum=gear_addendum,
                clearance=planet_clearance,
                circular_pitch=circular_pitch
        )
        self.target_gear_ratio = target_gear_ratio
        self.num_results = num_results
        self.use_abs = use_abs
        self.fixed = fixed
        self.input = input
        self.output = output

        self._abort = False

    def run(self):
        def update_progress(value):
            self.progress_updated.emit(value)

        def is_aborted():
            return self._abort

        results = evaluate_and_search_2d(self.constraints,
                           self.target_gear_ratio, update_progress, num_results=self.num_results, use_abs=self.use_abs,
                                         fixed=self.fixed, input=self.input, output=self.output)
        if results is not None:
            self.finished.emit(results)

    def abort(self):
        """Signals the worker thread to stop."""
        self._abort = True

