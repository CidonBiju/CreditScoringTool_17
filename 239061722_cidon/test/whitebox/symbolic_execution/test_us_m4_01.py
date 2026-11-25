import unittest

from decision.risk_decision import classify_risk_category
from ...fixtures import profile


class TestSymbolicExecution(unittest.TestCase):
    def test_solutions_to_path_constraints(self):
        # Columns are score, DTI, utilisation, severe events, output.
        cases = (
            ("E >= 1", 800, 20, 30, 1, "High Risk"),
            ("E = 0, D >= 60", 800, 60, 30, 0, "High Risk"),
            ("E = 0, D < 60, S < 600", 599, 20, 30, 0, "High Risk"),
            ("S >= 600, 40 <= D < 60, U >= 75, E = 0", 800, 40, 75, 0, "High Risk"),
            ("600 <= S < 650, D < 40, U >= 75, E = 0", 649, 39, 75, 0, "High Risk"),
            ("600 <= S < 650, D < 40, U < 75, E = 0", 625, 20, 30, 0, "Subprime"),
            ("650 <= S < 700, 40 <= D < 60, U < 75, E = 0", 650, 40, 30, 0, "Subprime"),
            ("S >= 700, 40 <= D < 60, U < 75, E = 0", 700, 40, 30, 0, "Near Prime"),
            ("S >= 700, D < 40, U = None, E = 0", 700, 20, None, 0, "Near Prime"),
            ("S >= 700, D < 40, U < 75, E = 0", 700, 20, 30, 0, "Prime"),
        )
        for constraint, score, dti, utilisation, events, expected in cases:
            with self.subTest(constraint=constraint):
                self.assertEqual(
                    classify_risk_category(score, profile(dti, utilisation, events)), expected
                )
