import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_hierarchical_cycles_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class HierarchicalCyclesEvalTest(unittest.TestCase):
    def test_child_response_within_budget_validates(self):
        response = ev.ChildResponse("vision", "evidence", 3, 5, evidence_refs=("evidence:vision",))
        ev.validate_child_response(response)

    def test_budget_overrun_rejected(self):
        response = ev.ChildResponse("vision", "evidence", 6, 5, evidence_refs=("evidence:vision",))
        with self.assertRaises(ValueError):
            ev.validate_child_response(response)

    def test_child_final_authority_rejected(self):
        response = ev.ChildResponse("planner", "proposal", 3, 5, proposal_refs=("proposal:a",), final_authority=True)
        with self.assertRaises(ValueError):
            ev.validate_child_response(response)

    def test_parent_trace_preserves_deferred_child(self):
        responses = (
            ev.ChildResponse("vision", "evidence", 3, 5, evidence_refs=("evidence:vision",)),
            ev.ChildResponse("route", "deferred", 5, 5),
        )
        trace = ev.parent_trace("parent:1", responses)
        self.assertEqual(trace["deferred"], ["route"])
        self.assertIn("evidence:vision", trace["evidence_refs"])

    def test_proposal_response_requires_proposal_ref(self):
        response = ev.ChildResponse("planner", "proposal", 3, 5)
        with self.assertRaises(ValueError):
            ev.validate_child_response(response)


if __name__ == "__main__":
    unittest.main()
