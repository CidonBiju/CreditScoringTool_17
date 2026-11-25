import unittest
from random import Random

from decision.risk_decision import classify_risk_category
from ...fixtures import profile


class TestRandomBased(unittest.TestCase):
    def test_generated_profiles_against_decision_table(self):
        random = Random(4101)
        # Rows represent score bands. Columns represent warning counts 0, 1, 2.
        decision_table = (
            ("High Risk", "High Risk", "High Risk"),
            ("Subprime", "High Risk", "High Risk"),
            ("Subprime", "Subprime", "High Risk"),
            ("Prime", "Near Prime", "High Risk"),
        )
        for sample in range(1000):
            score = random.randint(300, 850)
            dti = random.randint(0, 10000) / 100
            utilisation = random.choice((None, random.randint(0, 10000) / 100))
            severe_events = random.choice((0, 0, 0, 1, 2))
            band = sum(score >= cutoff for cutoff in (600, 650, 700))
            warning_count = sum((dti >= 40, utilisation is not None and utilisation >= 75))
            expected = decision_table[band][warning_count]
            if severe_events or dti >= 60:
                expected = "High Risk"
            elif expected == "Prime" and utilisation is None:
                expected = "Near Prime"
            with self.subTest(sample=sample, score=score, dti=dti,
                              utilisation=utilisation, severe_events=severe_events):
                self.assertEqual(
                    classify_risk_category(score, profile(dti, utilisation, severe_events)),
                    expected,
                )
