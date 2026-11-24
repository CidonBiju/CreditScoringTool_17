import unittest

from scoring.credit_scoring import apply_weighting_profile


class TestWeightingProfiles(unittest.TestCase):
    def setUp(self):
        self.metrics = {
            "dti": 60.0,
            "overall_utilisation": {"utilisation": 60.0},
            "payment_history": {"consistency_score": 90.0},
        }

    def test_supported_profiles_apply_their_agreed_weights(self):
        # Each supported profile has its own expected score for the same applicant.
        for profile, expected in [("Conservative", 630), ("High Risk", 685)]:
            with self.subTest(profile=profile):
                result = apply_weighting_profile(self.metrics, profile)
                self.assertEqual(result["score"], expected)

    def test_zero_payment_consistency_is_valid(self):
        self.metrics["payment_history"]["consistency_score"] = 0.0
        result = apply_weighting_profile(self.metrics, "Conservative")
        self.assertEqual(result["score"], 432)

    def test_missing_payment_consistency_reports_insufficient_history(self):
        self.metrics["payment_history"]["consistency_score"] = None
        with self.assertRaisesRegex(ValueError, "Insufficient payment history"):
            apply_weighting_profile(self.metrics, "Conservative")