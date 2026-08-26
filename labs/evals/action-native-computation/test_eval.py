import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_action_native_computation_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class ActionNativeComputationEvalTests(unittest.TestCase):
    def test_declared_action_produces_visible_update_direction(self):
        subject = ev.HeatRelaxationSubject()
        state = (100.0, 60.0, 40.0, 0.0)
        direction = subject.update_direction(state)
        next_state = subject.step(state)

        self.assertEqual(0.0, direction[0])
        self.assertEqual(0.0, direction[3])
        self.assertNotEqual(0.0, direction[1])
        self.assertNotEqual(0.0, direction[2])
        self.assertLess(subject.action(next_state), subject.action(state))

    def test_repeated_evolution_does_not_increase_action(self):
        run = ev.run_action_native_heat_eval()
        for before, after in zip(run.action_values, run.action_values[1:]):
            self.assertLessEqual(after, before + 1e-9)

    def test_boundary_constraints_stay_fixed(self):
        run = ev.run_action_native_heat_eval()
        for state in run.states:
            self.assertEqual(100.0, state[0])
            self.assertEqual(0.0, state[3])

    def test_residual_and_error_are_reported(self):
        run = ev.run_action_native_heat_eval()
        self.assertIn("residual", run.readout)
        self.assertIn("error", run.readout)
        self.assertEqual(2, len(run.readout["residual"]))
        self.assertIsInstance(run.readout["error"], float)

    def test_readout_is_accepted_only_after_validation_passes(self):
        subject = ev.HeatRelaxationSubject(tolerance=1e-4)
        initial_readout = subject.trusted_readout((100.0, 60.0, 40.0, 0.0))
        final_run = subject.run(steps=32)

        self.assertFalse(initial_readout["accepted"])
        self.assertTrue(final_run.readout["accepted"])
        self.assertLessEqual(final_run.readout["error"], subject.tolerance)

    def test_missing_action_is_rejected(self):
        subject = ev.HeatRelaxationSubject(action_declared=False)
        with self.assertRaises(ev.MissingActionError):
            subject.action((100.0, 60.0, 40.0, 0.0))
        with self.assertRaises(ev.MissingActionError):
            subject.update_direction((100.0, 60.0, 40.0, 0.0))

    def test_hidden_forcing_is_rejected_unless_declared(self):
        hidden = ev.HeatRelaxationSubject(source={1: 5.0}, source_declared=False)
        with self.assertRaises(ev.HiddenForcingError):
            hidden.step((100.0, 60.0, 40.0, 0.0))

        declared = ev.HeatRelaxationSubject(source={1: 5.0}, source_declared=True)
        next_state = declared.step((100.0, 60.0, 40.0, 0.0))
        self.assertEqual(75.0, next_state[1])

    def test_readout_cannot_claim_authority_without_residual_and_validation(self):
        subject = ev.HeatRelaxationSubject()
        with self.assertRaises(ev.ReadoutAuthorityError):
            subject.trusted_readout((100.0, 60.0, 40.0, 0.0), include_residual=False)
        with self.assertRaises(ev.ReadoutAuthorityError):
            subject.trusted_readout((100.0, 60.0, 40.0, 0.0), validate=False)

    def test_constraint_satisfaction_accepts_only_validated_assignment(self):
        subject = ev.ConstraintAssignmentSubject()
        readout = subject.solve()

        self.assertTrue(readout["accepted"])
        self.assertEqual(0, readout["residual"])
        self.assertIn(readout["assignment"], (
            {"a": "red", "b": "blue", "c": "red"},
            {"a": "blue", "b": "red", "c": "blue"},
        ))

    def test_constraint_satisfaction_rejects_invalid_assignment(self):
        subject = ev.ConstraintAssignmentSubject()
        invalid = {"a": "red", "b": "red", "c": "blue"}

        self.assertGreater(subject.action(invalid), 0)
        with self.assertRaises(ev.ConstraintViolationError):
            subject.trusted_readout(invalid)

    def test_constraint_satisfaction_requires_declared_action_and_validated_readout(self):
        missing = ev.ConstraintAssignmentSubject(action_declared=False)
        with self.assertRaises(ev.MissingActionError):
            missing.action({"a": "red", "b": "blue", "c": "red"})

        subject = ev.ConstraintAssignmentSubject()
        with self.assertRaises(ev.ReadoutAuthorityError):
            subject.trusted_readout({"a": "red", "b": "blue", "c": "red"}, include_residual=False)
        with self.assertRaises(ev.ReadoutAuthorityError):
            subject.trusted_readout({"a": "red", "b": "blue", "c": "red"}, validate=False)

    def test_least_action_path_selects_lowest_valid_path(self):
        subject = ev.LeastActionPathSubject()
        readout = subject.solve()

        self.assertTrue(readout["accepted"])
        self.assertEqual(("s", "a", "g"), readout["path"])
        self.assertEqual(3.0, readout["action"])
        self.assertEqual(0, readout["residual"])

    def test_least_action_path_rejects_blocked_and_hidden_scoring(self):
        subject = ev.LeastActionPathSubject()
        blocked_path = ("s", "b", "d", "g")

        self.assertEqual(float("inf"), subject.action(blocked_path))
        with self.assertRaises(ev.ConstraintViolationError):
            subject.trusted_readout(blocked_path)

        hidden = ev.LeastActionPathSubject(weights_declared=False)
        with self.assertRaises(ev.HiddenScoringError):
            hidden.action(("s", "a", "g"))

    def test_least_action_path_requires_declared_action_and_validated_readout(self):
        missing = ev.LeastActionPathSubject(action_declared=False)
        with self.assertRaises(ev.MissingActionError):
            missing.action(("s", "a", "g"))

        subject = ev.LeastActionPathSubject()
        with self.assertRaises(ev.ReadoutAuthorityError):
            subject.trusted_readout(("s", "a", "g"), include_residual=False)
        with self.assertRaises(ev.ReadoutAuthorityError):
            subject.trusted_readout(("s", "a", "g"), validate=False)


if __name__ == "__main__":
    unittest.main()
