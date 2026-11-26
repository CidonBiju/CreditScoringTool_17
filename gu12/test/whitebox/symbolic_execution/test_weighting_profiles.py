import unittest

from scoring.credit_scoring import apply_weighting_profile


class TestSymbolicWeightingProfiles(unittest.TestCase):
    def test_error_paths_from_symbolic_tree(self):
        # Each case passes the earlier decisions and fails at its named endpoint
        cases = [
            ("P1", "Unknown", 90, 60, 60, "Unknown weighting profile: Unknown"),
            ("P2", "Conservative", None, 60, 60, "Insufficient payment history"),
            ("P3", "Conservative", "90", 60, 60,
             "payment_history must be a number between 0 and 100"),
            ("P4", "Conservative", 90, 101, 60,
             "dti must be a number between 0 and 100"),
            ("P5", "Conservative", 90, 60, 101,
             "utilisation must be a number between 0 and 100"),
        ]

        for path, profile, payment, dti, utilisation, expected in cases:
            with self.subTest(path=path):
                metrics = {
                    "payment_history": {"consistency_score": payment},
                    "dti": dti,
                    "overall_utilisation": {"utilisation": utilisation},
                }
                with self.assertRaises(ValueError) as raised:
                    apply_weighting_profile(metrics, profile)
                self.assertEqual(str(raised.exception), expected)

    def test_p6_returns_a_score_for_each_profile(self):
        metrics = {
            "payment_history": {"consistency_score": 90},
            "dti": 60,
            "overall_utilisation": {"utilisation": 60},
        }
        for profile, expected in [("Conservative", 630), ("High Risk", 685)]:
            with self.subTest(profile=profile):
                result = apply_weighting_profile(metrics, profile)
                self.assertEqual(result["score"], expected)
                self.assertEqual(result["profile"], profile)