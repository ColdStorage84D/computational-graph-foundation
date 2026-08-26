import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_visual_media_encoding_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class VisualMediaEncodingEvalTest(unittest.TestCase):
    def test_region_preserves_source_and_frame(self):
        region = ev.Region("region:1", "frame:0", (1, 2, 3, 4), "media:sample", 0.8)
        ev.validate_region(region)
        self.assertEqual(region.frame_ref, "frame:0")
        self.assertEqual(region.source_ref, "media:sample")

    def test_invalid_bbox_rejected(self):
        with self.assertRaises(ValueError):
            ev.validate_region(ev.Region("region:bad", "frame:0", (1, 1, 0, 4), "media:sample", 0.8))

    def test_track_preserves_region_and_source_refs(self):
        regions = (
            ev.Region("region:1", "frame:0", (1, 2, 3, 4), "media:sample", 0.8),
            ev.Region("region:2", "frame:1", (2, 2, 3, 4), "media:sample", 0.7),
        )
        track = ev.build_track("track:1", regions)
        self.assertEqual(track.region_refs, ("region:1", "region:2"))
        self.assertEqual(track.source_refs, ("media:sample", "media:sample"))

    def test_graph_view_keeps_evidence_refs(self):
        regions = (ev.Region("region:1", "frame:0", (1, 2, 3, 4), "media:sample", 0.8),)
        view = ev.graph_view_from_regions("view:1", regions)
        self.assertEqual(view["node_refs"], ["region:1"])
        self.assertEqual(view["evidence_refs"], ["media:sample"])

    def test_confidence_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            ev.validate_region(ev.Region("region:bad", "frame:0", (1, 2, 3, 4), "media:sample", 1.4))


if __name__ == "__main__":
    unittest.main()
