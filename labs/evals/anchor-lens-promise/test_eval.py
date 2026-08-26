import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_anchor_lens_promise_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class AnchorLensPromiseEvalTest(unittest.TestCase):
    def test_same_application_has_stable_id(self):
        app = ev.LensApplication("anchor:1", "v1", "region-lens", "1.0", {"threshold": 0.4})
        self.assertEqual(ev.stable_lens_application_id(app), ev.stable_lens_application_id(app))

    def test_lens_version_changes_identity(self):
        first = ev.LensApplication("anchor:1", "v1", "region-lens", "1.0", {"threshold": 0.4})
        second = ev.LensApplication("anchor:1", "v1", "region-lens", "1.1", {"threshold": 0.4})
        self.assertNotEqual(ev.stable_lens_application_id(first), ev.stable_lens_application_id(second))

    def test_pending_promise_has_no_output(self):
        promise = ev.Promise("lensapp:a", "pending")
        ev.validate_promise(promise)
        with self.assertRaises(ValueError):
            ev.validate_promise(ev.Promise("lensapp:a", "pending", "view:a"))

    def test_fulfilled_promise_requires_output_and_evidence(self):
        promise = ev.Promise("lensapp:a", "pending")
        fulfilled = ev.fulfill_promise(promise, "view:a", ("anchor:1",))
        self.assertEqual(fulfilled.status, "fulfilled")
        self.assertEqual(fulfilled.output_ref, "view:a")
        self.assertIn("anchor:1", fulfilled.evidence_refs)

    def test_invalid_status_rejected(self):
        with self.assertRaises(ValueError):
            ev.validate_promise(ev.Promise("lensapp:a", "unknown"))


if __name__ == "__main__":
    unittest.main()
