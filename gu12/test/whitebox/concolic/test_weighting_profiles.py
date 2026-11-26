import unittest

from scoring.credit_scoring import apply_weighting_profile


class TestConcolicWeightingProfiles(unittest.TestCase):
    def test_reverse_utilisation_decision_from_p6_to_p5(self):
        metrics = {
            "payment_history": {"consistency_score": 90},
            "dti": 60,
            "overall_utilisation": {"utilisation": 60},
        }

        result = apply_weighting_profile(metrics, "Conservative")
        self.assertEqual(result["score"], 630)

        # Preserve the earlier decisions and reverse the final range check
        metrics["overall_utilisation"]["utilisation"] = 101

        with self.assertRaises(ValueError) as raised:
            apply_weighting_profile(metrics, "Conservative")
        self.assertEqual(
            str(raised.exception),
            "utilisation must be a number between 0 and 100",
        )