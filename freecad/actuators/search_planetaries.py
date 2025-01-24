from rtree import index
from fractions import Fraction
import math
from itertools import permutations

def evaluate_gear_ratio(planet_teeth: int, sun_teeth: int, fixed: str, input_: str, output: str) -> float:
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
            return 1 + sun_teeth / ring_teeth
        elif input_ == "Carrier" and output == "Ring":
            return (ring_teeth / sun_teeth) + 1

    elif fixed == "Ring":
        if input_ == "Sun" and output == "Carrier":
            return 1 + ring_teeth / sun_teeth
        elif input_ == "Carrier" and output == "Sun":
            return sun_teeth / (ring_teeth + sun_teeth)

    elif fixed == "Carrier":
        if input_ == "Sun" and output == "Ring":
            return -ring_teeth / sun_teeth  # Negative indicates direction reversal
        elif input_ == "Ring" and output == "Sun":
            return -sun_teeth / ring_teeth  # Negative indicates direction reversal

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
        remaining_options = list(set(possible_values) - set(known_slots))
        slot_combinations = [tuple([remaining_options[i] if fixed == "Any" else fixed,
                                    remaining_options[1 - i] if input_ == "Any" else input_,
                                    output])
                             for i in range(2)]

    # If all three are Any, generate all permutations
    elif len(any_slots) == 3:
        slot_combinations = list(permutations(possible_values, 3))

    else:
        # No 'Any' values, just evaluate the given configuration
        slot_combinations = [(fixed, input_, output)]

    results = {}
    for fixed_val, input_val, output_val in slot_combinations:
        try:
            ratio = evaluate_gear_ratio(planet_teeth, sun_teeth, fixed_val, input_val, output_val)
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
    nearest_items_it = idx.nearest((target_value, 0, target_value,0), num_results=num_results, objects=True)
    nearest_items_list = []
    for n in nearest_items_it:
        nearest_items_list.append(n.object)  # Combine the actual value with a, b, x, y values
    nearest_items_list.sort(key=lambda x: abs(x['gear_ratio']-target_value))
    #print("found closest matches")
    return nearest_items_list


def evaluate_and_search_2d(min_planet_teeth, max_planet_teeth,
                           min_sun_teeth, max_sun_teeth,
                           target_gear_ratio, update_progress, num_results=1, num_planets = 3,
                           addendum=None, clearance=0.5, circular_pitch=4.0, use_abs=False):
    # Create an R-tree index
    p = index.Property()
    #p.dimension = 1
    idx = index.Index(properties=p)
    if addendum is None:
        addendum = circular_pitch/math.pi  # addendum = module typically

    full = (max_planet_teeth + 1 - min_planet_teeth) * (max_sun_teeth + 1 - min_sun_teeth)
    # Evaluate the function and store results in the R-tree
    for planet_teeth in range(min_planet_teeth, max_planet_teeth + 1):
        for sun_teeth in range(min_sun_teeth, max_sun_teeth + 1):
            partial = (planet_teeth - min_planet_teeth) * (max_sun_teeth + 1 - min_sun_teeth) + (sun_teeth - min_sun_teeth)
            if update_progress is not None:
                update_progress((partial/full)*100.0)
            is_homo = _is_homogeneity_distribution_constraint_satisfied(sun_teeth, planet_teeth, num_planets)
            is_good_neighbor = _is_neighbor_constraint_satisfied(sun_teeth, planet_teeth, num_planets, addendum, clearance, circular_pitch)
            if not (is_homo and is_good_neighbor):
                continue
            result = evaluate_all_possible_ratios(planet_teeth, sun_teeth, 'Any', 'Any', 'Any')
            for r_gear, r_val in result.items():
                abs_res = abs(r_val) if use_abs else r_val
                idx.insert(0, (abs_res, 0,abs_res,0), obj={"gear_ratio":abs_res, "Planet Teeth":planet_teeth, "Sun Teeth":sun_teeth, "Fixed":r_gear[0], "Input":r_gear[1], "Output":r_gear[2]})
    # print("finding closest matches")
    # Perform the search for the closest match
    return _find_closest_matches(idx, target_gear_ratio, num_results)


if __name__ == "__main__":
    min_sun_1_teeth, max_sun_1_teeth = 8, 12
    min_planet_1_teeth, max_planet_1_teeth = 6, 24

    target_gear_ratio = 1./5
    import time
    t0 = time.time()
    # ring 2 is the output, so 2 is the secondary
    # the list is: [result, planet_2_teeth, sun_2_teeth, planet_1_teeth, sun_1_teeth]
    # so the last two items are the first gearbox
    module = 1.5
    circular_pitch = module*math.pi
    closest_match = evaluate_and_search_2d(min_planet_1_teeth, max_planet_1_teeth,
                                           min_sun_1_teeth, max_sun_1_teeth,
                                           target_gear_ratio, num_results=10, use_abs=False,
                                           clearance=0.5, # mm
                                           num_planets=4, circular_pitch=circular_pitch)  # use 3 for higher gear ratios but lower stability. 4 can get some good precision
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

    def __init__(self, min_planet_teeth, max_planet_teeth, min_sun_teeth, max_sun_teeth, target_gear_ratio, gear_addendum, planet_clearance, num_results, num_planets, circular_pitch, use_abs):
        super().__init__()
        self.min_planet_teeth = min_planet_teeth
        self.max_planet_teeth = max_planet_teeth
        self.min_sun_teeth = min_sun_teeth
        self.max_sun_teeth = max_sun_teeth
        self.target_gear_ratio = target_gear_ratio
        self.gear_addendum = gear_addendum
        self.planet_clearance = planet_clearance
        self.num_results = num_results
        self.num_planets = num_planets
        self.circular_pitch = circular_pitch
        self.use_abs = use_abs
        self._abort = False

    def run(self):
        def update_progress(value):
            self.progress_updated.emit(value)

        def is_aborted():
            return self._abort

        results = evaluate_and_search_2d(self.min_planet_teeth, self.max_planet_teeth,
                           self.min_sun_teeth, self.max_sun_teeth,
                           self.target_gear_ratio, update_progress, num_results=self.num_results, num_planets = self.num_planets,
                           addendum=self.gear_addendum, clearance=self.planet_clearance, circular_pitch=self.circular_pitch, use_abs=self.use_abs)
        if results is not None:
            self.finished.emit(results)

    def abort(self):
        """Signals the worker thread to stop."""
        self._abort = True

