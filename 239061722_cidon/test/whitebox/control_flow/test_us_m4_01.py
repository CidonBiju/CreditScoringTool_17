import unittest

from decision.risk_decision import classify_risk_category
from ...fixtures import profile


class TestControlFlow(unittest.TestCase):
    def test_classification_paths(self):
        cases = (
            (750, 20, 30, 0, "Prime"),
            (750, 20, 30, 1, "High Risk"),
            (750, 60, 30, 0, "High Risk"),
            (599, 20, 30, 0, "High Risk"),
            (750, 40, 30, 0, "Near Prime"),
            (750, 20, None, 0, "Near Prime"),
            (750, 20, 75, 0, "Near Prime"),
            (750, 40, 75, 0, "High Risk"),
            (649, 40, 30, 0, "High Risk"),
            (649, 20, 30, 0, "Subprime"),
            (699, 20, 30, 0, "Subprime"),
            (750, 40, None, 0, "Near Prime"),
            (599, 20, None, 0, "High Risk"),
            (650, 20, 75, 0, "Subprime"),
        )
        for score, dti, utilisation, events, expected in cases:
            with self.subTest(score=score, dti=dti, utilisation=utilisation, events=events):
                self.assertEqual(
                    classify_risk_category(score, profile(dti, utilisation, events)), expected
                )

    def test_validation_paths(self):
        cases = (
            ("750", profile()), (299, profile()), (750, {}),
            (750, {"dti": 20}), (750, {"dti": 20, "overall_utilisation": {"utilisation": 30}}),
            (750, profile(dti=None)), (750, profile(dti=-1)), (750, profile(dti=101)),
            (750, profile(utilisation="75")), (750, profile(utilisation=-1)),
            (750, profile(utilisation=101)), (750, profile(severe_events=None)),
            (750, profile(severe_events=-1)),
        )
        for score, metrics in cases:
            with self.subTest(score=score, metrics=metrics), self.assertRaises(ValueError):
                classify_risk_category(score, metrics)
