import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_local_voting_world_model_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class LocalVotingWorldModelEvalTest(unittest.TestCase):
    def test_path_integration_binds_features_to_locations(self):
        column = ev.PredictiveColumn("probe-column")
        events = column.learn_from(ev.OBJECT_LIBRARY["object:cup"])

        self.assertEqual((0, 0), events[0].reference_position)
        self.assertEqual("handle_curve", events[0].feature_input)
        self.assertEqual((1, 0), events[1].action_output)
        self.assertEqual((2, 0), events[2].reference_position)
        self.assertEqual("rim_arc", column.object_maps["object:cup"][(2, 0)])

    def test_single_column_observations_are_ambiguous(self):
        result = ev.run_fixture()
        thumb = next(item for item in result.observations if item.column_id == "thumb-column")
        index = next(item for item in result.observations if item.column_id == "index-column")

        self.assertEqual("handle_curve", thumb.feature)
        self.assertIn("object:cup", thumb.candidate_object_refs)
        self.assertGreater(len(thumb.candidate_object_refs), 1)
        self.assertEqual("rim_arc", index.feature)
        self.assertIn("object:cup", index.candidate_object_refs)
        self.assertGreater(len(index.candidate_object_refs), 1)

    def test_lateral_voting_converges_on_shared_object(self):
        result = ev.run_fixture()

        self.assertEqual("object:cup", result.voting.selected_object_ref)
        self.assertIn("object:drawer", result.voting.rejected_object_refs)
        self.assertIn("object:saucer", result.voting.rejected_object_refs)
        self.assertGreater(result.voting.selected_margin, 4.0)

    def test_voting_trace_preserves_column_level_scores(self):
        result = ev.run_fixture()
        initial = result.voting.vote_rounds[0].column_scores
        final = result.voting.vote_rounds[-1].column_scores

        self.assertIn("object:drawer", initial["thumb-column"])
        self.assertIn("object:saucer", initial["index-column"])
        self.assertGreater(final["thumb-column"]["object:cup"], final["thumb-column"]["object:drawer"])
        self.assertGreater(final["index-column"]["object:cup"], final["index-column"]["object:saucer"])

    def test_prediction_uses_selected_object_location_and_action(self):
        result = ev.run_fixture()

        self.assertEqual("object:cup", result.prediction.object_ref)
        self.assertEqual((2, 0), result.prediction.from_position)
        self.assertEqual((0, 1), result.prediction.action_delta)
        self.assertEqual((2, 1), result.prediction.target_position)
        self.assertEqual("hollow_ceramic", result.prediction.predicted_feature)
        self.assertTrue(result.prediction.matched)

    def test_claim_boundary_does_not_present_world_model_ai_as_solved(self):
        result = ev.run_fixture()

        self.assertIn("Toy graph mechanism only", result.claim_boundary)
        self.assertIn("No real-world performance claim", result.claim_boundary)


if __name__ == "__main__":
    unittest.main()
