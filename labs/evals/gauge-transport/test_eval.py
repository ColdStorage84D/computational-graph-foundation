import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_gauge_transport_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class GaugeTransportEvalTest(unittest.TestCase):
    def frames(self):
        root = ev.declare_frame("root", ("x", "y"))
        child = ev.declare_frame("child", ("u", "v"))
        return root, child

    def test_identity_transport_preserves_state(self):
        root, _ = self.frames()
        transport = ev.TransportMap("id", root, root, ((1.0, 0.0), (0.0, 1.0)))
        self.assertEqual(ev.transport_state((2.0, 3.0), transport), (2.0, 3.0))

    def test_correct_and_wrong_transport_residuals_separate(self):
        root, child = self.frames()
        state = (2.0, 4.0)
        out = ev.TransportMap("scale", root, child, ((2.0, 0.0), (0.0, 2.0)))
        back = ev.invert_transport(out, "scale_inv")
        wrong = ev.TransportMap("wrong", child, root, ((0.25, 0.0), (0.0, 0.25)))
        self.assertLess(ev.score_residual(state, ev.transport_state(ev.transport_state(state, out), back)), 1e-9)
        self.assertGreater(ev.score_residual(state, ev.transport_state(ev.transport_state(state, out), wrong)), 1.0)

    def test_composed_transport_matches_two_step(self):
        root, child = self.frames()
        scale = ev.TransportMap("scale", root, child, ((2.0, 0.0), (0.0, 3.0)), ("scale-ref",))
        rotate = ev.TransportMap("rotate", child, root, ((0.0, -1.0), (1.0, 0.0)), ("rotate-ref",))
        composed = ev.compose_transport(scale, rotate, "composed")
        state = (1.0, 2.0)
        self.assertEqual(ev.transport_state(state, composed), ev.transport_state(ev.transport_state(state, scale), rotate))
        self.assertEqual(composed.source_refs, ("scale-ref", "rotate-ref"))

    def test_inverse_round_trip_recovers_source(self):
        root, child = self.frames()
        transport = ev.TransportMap("map", root, child, ((2.0, 1.0), (1.0, 1.0)))
        inverse = ev.invert_transport(transport, "map_inv")
        state = (5.0, 3.0)
        roundtrip = ev.transport_state(ev.transport_state(state, transport), inverse)
        self.assertLess(ev.score_residual(state, roundtrip), 1e-9)

    def test_invalid_inverse_and_dimensions_reject(self):
        root, child = self.frames()
        singular = ev.TransportMap("singular", root, child, ((1.0, 2.0), (2.0, 4.0)))
        with self.assertRaises(ValueError):
            ev.invert_transport(singular, "bad_inv")
        bad_shape = ev.TransportMap("bad", root, child, ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)))
        with self.assertRaises(ValueError):
            ev.transport_state((1.0, 2.0), bad_shape)

    def test_holonomy_flat_and_broken_loops(self):
        root, child = self.frames()
        out = ev.TransportMap("out", root, child, ((1.0, 0.0), (0.0, 1.0)))
        back = ev.TransportMap("back", child, root, ((1.0, 0.0), (0.0, 1.0)))
        broken = ev.TransportMap("broken", child, root, ((0.5, 0.0), (0.0, 0.5)))
        self.assertLess(ev.detect_holonomy((out, back), (1.0, 1.0)), 1e-9)
        self.assertGreater(ev.detect_holonomy((out, broken), (1.0, 1.0)), 0.1)


if __name__ == "__main__":
    unittest.main()
