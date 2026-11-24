import unittest

from scoring.credit_scoring import apply_weighting_profile


class TestPaymentConsistencyBoundaries(unittest.TestCase):
    """Boundary value analysis for issue #14, with DTI and utilisation fixed at 60%."""

    def setUp(self):
        self.metrics = {
            "dti": 60.0,
            "overall_utilisation": {"utilisation": 60.0},
            "payment_history": {"consistency_score": None},
        }

    def test_accepts_endpoints_and_values_just_inside(self):
        # In the Conservative profile each point of payment consistency adds
        # 2.2 credit-score points before rounding, starting from 432 at zero.
        for value, expected in [(0, 432), (0.01, 432), (99.99, 652), (100, 652)]:
            with self.subTest(consistency_score=value):
                self.metrics["payment_history"]["consistency_score"] = value
                result = apply_weighting_profile(self.metrics, "Conservative")
                self.assertEqual(result["score"], expected)

    def test_rejects_values_just_outside(self):
        for value in [-0.01, 100.01]:
            with self.subTest(consistency_score=value):
                self.metrics["payment_history"]["consistency_score"] = value
                with self.assertRaises(ValueError):
                    apply_weighting_profile(self.metrics, "Conservative")
