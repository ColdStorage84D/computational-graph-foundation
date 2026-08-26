import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_exterior_placement_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class ExteriorPlacementEvalTest(unittest.TestCase):
    def test_exterior_quantity_contributes_only_on_contact(self):
        internal = {"left", "right"}
        wind = ev.ExteriorQuantity("wind", "forcing", 2.0, ("left",))
        contribution = ev.exterior_contribution(internal, wind, {"left": 0.5})
        self.assertEqual(contribution["left"], 1.0)
        self.assertEqual(contribution["right"], 0.0)

    def test_exterior_does_not_enter_internal_state(self):
        internal_state = {"left": 1.0, "right": 2.0}
        wind = ev.ExteriorQuantity("wind", "forcing", 2.0, ("left",))
        self.assertEqual(ev.internal_state_without_exterior(internal_state, wind), internal_state)

    def test_missing_contact_rejected(self):
        wind = ev.ExteriorQuantity("wind", "forcing", 2.0, ())
        with self.assertRaises(ValueError):
            ev.validate_exterior_quantity({"left"}, wind)

    def test_unknown_contact_rejected(self):
        wind = ev.ExteriorQuantity("wind", "forcing", 2.0, ("missing",))
        with self.assertRaises(ValueError):
            ev.validate_exterior_quantity({"left"}, wind)

    def test_internal_leak_rejected(self):
        wind = ev.ExteriorQuantity("wind", "forcing", 2.0, ("left",))
        with self.assertRaises(ValueError):
            ev.internal_state_without_exterior({"left": 1.0, "wind": 2.0}, wind)


if __name__ == "__main__":
    unittest.main()
