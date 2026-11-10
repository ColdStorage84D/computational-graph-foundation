import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_causal_intervention_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


def contrast(model, **regime):
    return model.probability({"Y": 1}, **{k: {"X": 1} for k in regime}) - model.probability(
        {"Y": 1}, **{k: {"X": 0} for k in regime}
    )


class StructuralCausalModelTest(unittest.TestCase):
    def test_observing_and_intervening_give_different_answers(self):
        model = ev.confounded_model(1)
        self.assertAlmostEqual(model.probability({"Y": 1}, given={"X": 1}), 0.84)
        self.assertAlmostEqual(model.probability({"Y": 1}, do={"X": 1}), 0.60)
        # The observed contrast is almost six times the causal effect.
        self.assertAlmostEqual(contrast(model, given=True), 0.58)
        self.assertAlmostEqual(contrast(model, do=True), 0.10)

    def test_confounding_can_reverse_the_sign(self):
        model = ev.confounded_model(-1)
        self.assertGreater(contrast(model, given=True), 0.3)
        self.assertAlmostEqual(contrast(model, do=True), -0.10)

    def test_association_without_any_causal_effect(self):
        model = ev.confounded_model(0)
        self.assertGreater(contrast(model, given=True), 0.4)
        self.assertAlmostEqual(contrast(model, do=True), 0.0)

    def test_backdoor_adjustment_recovers_the_interventional_value(self):
        model = ev.confounded_model(1)
        adjusted = ev.backdoor_adjustment(
            model,
            treatment={"X": 1},
            outcome={"Y": 1},
            adjustment=("Z",),
            adjustment_values=(0, 1),
        )
        self.assertAlmostEqual(adjusted, model.probability({"Y": 1}, do={"X": 1}))
        # Adjusting for nothing is just conditioning, and stays biased.
        unadjusted = ev.backdoor_adjustment(
            model, treatment={"X": 1}, outcome={"Y": 1}, adjustment=(), adjustment_values=()
        )
        self.assertAlmostEqual(unadjusted, 0.84)

    def test_intervention_cuts_the_arrow_into_the_treatment(self):
        model = ev.confounded_model(1)
        self.assertAlmostEqual(model.probability({"Z": 1}, given={"X": 1}), 0.9)
        self.assertAlmostEqual(model.probability({"Z": 1}, do={"X": 1}), 0.5)

    def test_counterfactual_differs_from_intervention_on_a_fresh_unit(self):
        model = ev.confounded_model(1)
        counterfactual = model.counterfactual_probability(
            {"Y": 1}, evidence={"X": 1, "Y": 1}, do={"X": 0}
        )
        self.assertAlmostEqual(counterfactual, 74 / 84)
        self.assertAlmostEqual(model.probability({"Y": 1}, do={"X": 0}), 0.5)

    def test_model_rejects_undeclared_structure(self):
        with self.assertRaises(ValueError):
            ev.StructuralCausalModel(
                (ev.Mechanism("Y", ("X",), {0: 1.0}, lambda parents, noise: 0),)
            )
        with self.assertRaises(ValueError):
            ev.confounded_model(1).probability({"Y": 1}, do={"W": 1})
        with self.assertRaises(ValueError):
            ev.confounded_model(1).probability({"Y": 1}, given={"X": 2})

    def test_effect_record_carries_the_interventional_contrast(self):
        record = ev.effect_record(ev.confounded_model(1), "effect:x-y", treatment="X", outcome="Y")
        self.assertEqual(record.kind, "intervention")
        self.assertEqual(record.scope, ("X",))
        self.assertAlmostEqual(record.value, 0.10)


if __name__ == "__main__":
    unittest.main()
