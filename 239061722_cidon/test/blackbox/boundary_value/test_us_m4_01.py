import unittest

from decision.risk_decision import classify_risk_category
from ...fixtures import profile


class TestBoundaryValues(unittest.TestCase):
    def test_score_cutoffs(self):
        cases = (
            (599, 20, "High Risk"), (600, 20, "Subprime"), (601, 20, "Subprime"),
            (649, 45, "High Risk"), (650, 45, "Subprime"), (651, 45, "Subprime"),
            (699, 20, "Subprime"), (700, 20, "Prime"), (701, 20, "Prime"),
            (300, 20, "High Risk"), (850, 20, "Prime"),
        )
        for score, dti, expected in cases:
            with self.subTest(score=score):
                self.assertEqual(classify_risk_category(score, profile(dti=dti)), expected)

    def test_outside_score_range(self):
        for score in (299, 851):
            with self.subTest(score=score), self.assertRaises(ValueError):
                classify_risk_category(score, profile())

    def test_dti_cutoffs(self):
        for dti, expected in (
            (39.99, "Prime"), (40, "Near Prime"), (40.01, "Near Prime"),
            (59.99, "Near Prime"), (60, "High Risk"), (60.01, "High Risk"),
        ):
            with self.subTest(dti=dti):
                self.assertEqual(classify_risk_category(750, profile(dti=dti)), expected)

    def test_utilisation_cutoff(self):
        for utilisation, expected in (
            (74.99, "Prime"), (75, "Near Prime"), (75.01, "Near Prime"), (None, "Near Prime"),
        ):
            with self.subTest(utilisation=utilisation):
                self.assertEqual(
                    classify_risk_category(750, profile(utilisation=utilisation)), expected
                )

    def test_severe_event_cutoff(self):
        with self.assertRaises(ValueError):
            classify_risk_category(750, profile(severe_events=-1))
        self.assertEqual(classify_risk_category(750, profile(severe_events=0)), "Prime")
        self.assertEqual(classify_risk_category(750, profile(severe_events=1)), "High Risk")
