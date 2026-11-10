import importlib.util
import math
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_port_hamiltonian_flow_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()

NO_INPUT = (0.0,)


class PortHamiltonianSystemTest(unittest.TestCase):
    def test_lossless_system_conserves_energy(self):
        system = ev.mass_spring_damper(mass=2.0, stiffness=3.0, damping=0.0)
        run = ev.simulate(system, (1.0, 0.0), (NO_INPUT,) * 2000, dt=0.01)
        energies = run["energies"]
        self.assertAlmostEqual(energies[0], 1.5)
        self.assertLess(max(abs(value - energies[0]) for value in energies), 1e-10)
        self.assertEqual(run["dissipated"], 0.0)

    def test_damping_only_removes_energy_and_the_balance_closes(self):
        system = ev.mass_spring_damper(mass=1.0, stiffness=4.0, damping=0.5)
        run = ev.simulate(system, (1.0, 0.0), (NO_INPUT,) * 1500, dt=0.01)
        energies = run["energies"]
        self.assertTrue(all(later <= earlier + 1e-12 for earlier, later in zip(energies, energies[1:])))
        self.assertLess(energies[-1], 0.1 * energies[0])
        self.assertLess(run["worst_step_residual"], 1e-12)
        self.assertAlmostEqual(energies[0] - energies[-1], run["dissipated"], places=10)

    def test_port_supply_is_the_only_way_energy_enters(self):
        system = ev.mass_spring_damper(mass=1.0, stiffness=1.0, damping=0.2)
        inputs = tuple((math.sin(0.02 * index),) for index in range(1000))
        run = ev.simulate(system, (0.0, 0.0), inputs, dt=0.02)
        energies = run["energies"]
        self.assertGreater(run["supplied"], 0.0)
        self.assertLess(run["worst_step_residual"], 1e-12)
        self.assertAlmostEqual(
            energies[-1] - energies[0], run["supplied"] - run["dissipated"], places=10
        )

    def test_structure_violations_are_rejected(self):
        good = ev.mass_spring_damper(1.0, 1.0, 0.1)
        not_skew = ev.PortHamiltonianSystem(
            ((0.0, 1.0), (1.0, 0.0)), good.dissipation, good.storage, good.input_map
        )
        with self.assertRaises(ValueError):
            ev.validate_system(not_skew)
        with self.assertRaises(ValueError):
            ev.validate_system(ev.mass_spring_damper(1.0, 1.0, -0.1))
        with self.assertRaises(ValueError):
            ev.validate_system(ev.mass_spring_damper(1.0, -1.0, 0.1))

    def test_interconnection_is_power_conserving(self):
        composite = ev.interconnect(
            ev.mass_spring_damper(1.0, 2.0, 0.0), ev.mass_spring_damper(3.0, 0.5, 0.0)
        )
        ev.validate_system(composite)
        run = ev.simulate(composite, (1.0, 0.0, 0.0, 0.5), ((),) * 1500, dt=0.01)
        energies = run["energies"]
        self.assertLess(max(abs(value - energies[0]) for value in energies), 1e-10)
        # Energy really moves between the two subsystems.
        first_energy = 0.5 * (2.0 * run["final_state"][0] ** 2 + run["final_state"][1] ** 2)
        self.assertGreater(abs(first_energy - 1.0), 1e-3)

    def test_undeclared_loss_surfaces_as_an_accounting_residual(self):
        actual = ev.mass_spring_damper(1.0, 4.0, 0.5)
        run = ev.simulate(actual, (1.0, 0.0), (NO_INPUT,) * 500, dt=0.01)
        energies = run["energies"]
        declared = ev.balance_storage(
            energies[0], energies[-1], supply=run["supplied"], work=0.0, dissipation=0.0
        )
        honest = ev.balance_storage(
            energies[0], energies[-1], supply=run["supplied"], work=0.0, dissipation=run["dissipated"]
        )
        self.assertAlmostEqual(declared["residual"], -run["dissipated"], places=10)
        self.assertAlmostEqual(honest["residual"], 0.0, places=10)
        self.assertFalse(ev.flow_record(declared)["authority"])


if __name__ == "__main__":
    unittest.main()
