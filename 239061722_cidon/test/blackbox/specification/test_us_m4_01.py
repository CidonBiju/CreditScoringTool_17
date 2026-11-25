import unittest
from copy import deepcopy

from decision.risk_decision import classify_risk_category
from ...fixtures import profile


class TestSpecification(unittest.TestCase):
    def test_approved_rules(self):
        cases = (
            ("clean", 750, profile(), "Prime"),
            ("severe payment event", 800, profile(severe_events=1), "High Risk"),
            ("severe DTI", 800, profile(dti=65), "High Risk"),
            ("low score", 550, profile(), "High Risk"),
            ("two warnings", 800, profile(dti=45, utilisation=80), "High Risk"),
            ("borderline with DTI warning", 625, profile(dti=45), "High Risk"),
            ("borderline with utilisation warning", 625, profile(utilisation=80), "High Risk"),
            ("middle score", 675, profile(), "Subprime"),
            ("upper score with warning", 750, profile(utilisation=80), "Near Prime"),
            ("upper score with unknown utilisation", 750, profile(utilisation=None), "Near Prime"),
            ("unknown utilisation with severe DTI", 750, profile(dti=65, utilisation=None), "High Risk"),
        )
        for rule, score, metrics, expected in cases:
            with self.subTest(rule=rule):
                original = deepcopy(metrics)
                self.assertEqual(classify_risk_category(score, metrics), expected)
                self.assertEqual(metrics, original)

    def test_missing_or_malformed_profile(self):
        for metrics in (
            None, {}, {"dti": 20}, {"dti": 20, "overall_utilisation": {}},
            {"dti": 20, "overall_utilisation": None},
            {"dti": 20, "overall_utilisation": {"utilisation": None}},
            {"dti": 20, "overall_utilisation": {"utilisation": 30},
             "payment_history": {}},
        ):
            with self.subTest(metrics=metrics):
                with self.assertRaises(ValueError):
                    classify_risk_category(750, metrics)

    def test_invalid_values(self):
        cases = (
            (None, profile()), (True, profile()), (750.0, profile()),
            (750, profile(dti=-1)), (750, profile(dti=101)),
            (750, profile(dti=float("nan"))), (750, profile(dti="20")),
            (750, profile(utilisation=-1)), (750, profile(utilisation=101)),
            (750, profile(utilisation=float("inf"))), (750, profile(utilisation=True)),
            (750, profile(severe_events=-1)), (750, profile(severe_events=1.5)),
            (550, profile(dti=None, severe_events=1)),
        )
        for score, metrics in cases:
            with self.subTest(score=score, metrics=metrics):
                with self.assertRaises(ValueError):
                    classify_risk_category(score, metrics)
