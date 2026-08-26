import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_port_hamiltonian_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class PortHamiltonianFlowEvalTest(unittest.TestCase):
    def test_clean_storage_balance_has_zero_residual(self):
        balance = ev.balance_storage(50.0, 35.0, supply=0.0, work=10.0, dissipation=5.0)
        self.assertAlmostEqual(balance["residual"], 0.0)

    def test_overrun_surfaces_as_residual(self):
        balance = ev.balance_storage(50.0, 0.0, supply=0.0, work=48.0, dissipation=8.0)
        self.assertNotEqual(balance["residual"], 0.0)

    def test_dissipation_is_explicit(self):
        scored = ev.score_dissipation(20.0, 7.0)
        self.assertEqual(scored["consumed"], 27.0)
        self.assertEqual(scored["dissipation"], 7.0)

    def test_ports_compose_and_reject_mismatch(self):
        out_port = ev.Port("parent", "budget", "out")
        in_port = ev.Port("child", "budget", "in")
        exchange = ev.compose_ports(out_port, in_port, available=30.0, requested=50.0)
        self.assertEqual(exchange["exchanged"], 30.0)
        self.assertEqual(exchange["residual_request"], 20.0)
        with self.assertRaises(ValueError):
            ev.compose_ports(out_port, ev.Port("bad", "energy", "in"), 1.0, 1.0)

    def test_flow_record_has_no_authority(self):
        record = ev.flow_record(ev.balance_storage(10.0, 8.0, 0.0, 1.0, 1.0))
        self.assertFalse(record["authority"])


if __name__ == "__main__":
    unittest.main()
