import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_bayesian_filtering_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class BayesianFilteringEvalTest(unittest.TestCase):
    def test_predict_advances_state_and_uncertainty(self):
        prior = ev.GaussianState(0.0, 1.0)
        predicted = ev.predict(prior, velocity=2.0, dt=0.5, process_noise=0.25)
        self.assertAlmostEqual(predicted.mean, 1.0)
        self.assertGreater(predicted.covariance, prior.covariance)

    def test_update_moves_toward_measurement_and_reduces_uncertainty(self):
        predicted = ev.GaussianState(1.0, 2.0)
        posterior, innovation, gain = ev.update(predicted, measurement=2.0, measurement_noise=1.0)
        self.assertGreater(posterior.mean, predicted.mean)
        self.assertLess(posterior.covariance, predicted.covariance)
        self.assertAlmostEqual(innovation, 1.0)
        self.assertGreater(gain, 0.0)

    def test_higher_measurement_noise_lowers_gain(self):
        predicted = ev.GaussianState(1.0, 2.0)
        _, _, low_noise_gain = ev.update(predicted, measurement=2.0, measurement_noise=0.5)
        _, _, high_noise_gain = ev.update(predicted, measurement=2.0, measurement_noise=5.0)
        self.assertGreater(low_noise_gain, high_noise_gain)

    def test_normalized_innovation_rises_for_outlier(self):
        predicted = ev.GaussianState(1.0, 1.0)
        small = ev.normalized_innovation(0.2, predicted, measurement_noise=1.0)
        large = ev.normalized_innovation(4.0, predicted, measurement_noise=1.0)
        self.assertGreater(large, small)

    def test_invalid_noise_rejected(self):
        with self.assertRaises(ValueError):
            ev.update(ev.GaussianState(1.0, 1.0), measurement=2.0, measurement_noise=0.0)


if __name__ == "__main__":
    unittest.main()
