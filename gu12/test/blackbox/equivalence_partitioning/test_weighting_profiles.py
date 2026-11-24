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

    def test_unknown_profile_is_rejected(self):
        # Invalid profile partition: otherwise valid metrics isolate this input.
        with self.assertRaisesRegex(ValueError, r"^Unknown weighting profile: Unknown$"):
            apply_weighting_profile(self.metrics, "Unknown")

    def test_each_profile_returns_its_signed_score_breakdown(self):
        # For the same applicant, check each profile against hand-calculated points.
        expected_breakdowns = {
            "Conservative": {"payment_history": 88.0, "dti": -19.25, "utilisation": -13.75},
            "High Risk": {"payment_history": 132.0, "dti": -13.75, "utilisation": -8.25},
        }
        for profile, expected in expected_breakdowns.items():
            with self.subTest(profile=profile):
                result = apply_weighting_profile(self.metrics, profile)
                self.assertEqual(result["profile"], profile)
                self.assertEqual(result["score_breakdown"].keys(), expected.keys())
                for factor, points in expected.items():
                    self.assertAlmostEqual(result["score_breakdown"][factor], points)
