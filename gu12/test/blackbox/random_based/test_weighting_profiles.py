"""Seeded, specification-based random inputs for issue #14."""

import random
import unittest
from fractions import Fraction

from scoring.credit_scoring import apply_weighting_profile


class TestRandomWeightingProfiles(unittest.TestCase):
    def test_scores_match_the_agreed_weights(self):
        rng = random.Random(1401)
        profiles = {"Conservative": (40, 35, 25), "High Risk": (60, 25, 15)}

        for case in range(100):
            # One unit is 0.01 percentage points. Keep the oracle exact.
            payment, dti, utilisation = (rng.randint(0, 10000) for _ in range(3))
            metrics = {
                "payment_history": {"consistency_score": payment / 100},
                "dti": dti / 100,
                "overall_utilisation": {"utilisation": utilisation / 100},
            }
            for profile, (wp, wd, wu) in profiles.items():
                with self.subTest(case=case, profile=profile, metrics=metrics):
                    weighted = wp * payment + wd * (10000 - dti) + wu * (10000 - utilisation)
                    expected = round(300 + 550 * Fraction(weighted, 1000000))
                    result = apply_weighting_profile(metrics, profile)
                    self.assertEqual(result["score"], expected)
