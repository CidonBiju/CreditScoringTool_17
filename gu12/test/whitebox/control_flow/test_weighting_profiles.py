"""Exercise the scorer's guards and validation loop with seeded values."""

import random
import unittest

from scoring.credit_scoring import apply_weighting_profile


class TestWeightingControlFlow(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(1402)

    def valid_metrics(self):
        return {
            "payment_history": {"consistency_score": self.rng.randint(0, 100)},
            "dti": self.rng.randint(0, 100),
            "overall_utilisation": {"utilisation": self.rng.randint(0, 100)},
        }

    def test_profile_guard_runs_before_metric_lookup(self):
        unknown = f"Unknown-{self.rng.randrange(10000)}"
        with self.assertRaisesRegex(ValueError, "Unknown weighting profile"):
            apply_weighting_profile({}, unknown)

    def test_missing_history_exits_before_validation_loop(self):
        metrics = {"payment_history": {"consistency_score": None}}
        with self.assertRaisesRegex(ValueError, "Insufficient payment history"):
            apply_weighting_profile(metrics, "Conservative")

    def test_loop_rejects_invalid_values_at_each_position(self):
        for name in ("payment_history", "dti", "utilisation"):
            below = -self.rng.randint(1, 100)
            above = 100 + self.rng.randint(1, 100)
            for invalid in (below, above, str(self.rng.randint(0, 100)), False):
                with self.subTest(metric=name, value=invalid):
                    metrics = self.valid_metrics()
                    if name == "payment_history":
                        metrics[name]["consistency_score"] = invalid
                    elif name == "utilisation":
                        metrics["overall_utilisation"][name] = invalid
                    else:
                        metrics[name] = invalid
                    with self.assertRaisesRegex(ValueError, f"^{name} must be a number"):
                        apply_weighting_profile(metrics, "Conservative")

    def test_loop_finishes_and_returns_all_contributions(self):
        for profile in ("Conservative", "High Risk"):
            with self.subTest(profile=profile):
                result = apply_weighting_profile(self.valid_metrics(), profile)
                self.assertEqual(result["profile"], profile)
                self.assertEqual(set(result["score_breakdown"]), {"payment_history", "dti", "utilisation"})
                self.assertEqual(result["score"], round(575 + sum(result["score_breakdown"].values())))
