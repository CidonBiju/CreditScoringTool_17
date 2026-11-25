import unittest

from decision.risk_decision import classify_risk_category
from ...fixtures import profile


class TestConcolic(unittest.TestCase):
    def test_negate_one_condition_from_each_seed_path(self):
        # The follow-up input changes one value and preserves the earlier
        # decisions up to the named condition.
        pairs = (
            ("score < 700", (699, 20, 30, 0), "Subprime", 0, 700, "Prime"),
            ("score < 650", (649, 40, 30, 0), "High Risk", 0, 650, "Subprime"),
            ("utilisation >= 75", (800, 40, 74.99, 0), "Near Prime", 2, 75, "High Risk"),
            ("DTI >= 60", (800, 59.99, 30, 0), "Near Prime", 1, 60, "High Risk"),
            ("severe events >= 1", (800, 20, 30, 0), "Prime", 3, 1, "High Risk"),
            ("utilisation is not None in validation", (800, 20, 30, 0), "Prime",
             2, None, "Near Prime"),
        )
        for condition, seed, expected_seed, field, replacement, expected_follow_up in pairs:
            score, dti, utilisation, events = seed
            with self.subTest(condition=condition, role="seed"):
                self.assertEqual(
                    classify_risk_category(score, profile(dti, utilisation, events)),
                    expected_seed,
                )
            # Solve the negated condition by substituting its alternate value.
            follow_up = list(seed)
            follow_up[field] = replacement
            score, dti, utilisation, events = follow_up
            with self.subTest(condition=condition, role="negated"):
                self.assertEqual(
                    classify_risk_category(score, profile(dti, utilisation, events)),
                    expected_follow_up,
                )
