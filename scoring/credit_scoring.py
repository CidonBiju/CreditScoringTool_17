"""Module 3 - Scoring Algorithm.

Owner: Gokul. User stories US-M3-01 to US-M3-09.

Uses the Module 2 metrics profile to produce and explain the final
credit score (300 to 850).
"""

from ingestion.credit_applicant import CreditApplicant


def rank_score_factors(score_breakdown: dict) -> dict:
    """US-M3-01: Rank the top three positive and negative score factors.

    Args:
        score_breakdown: Points each metric added to or removed from
            the score, e.g. {"dti": 40, "late_payments": -60}.

    Returns:
        {"top_positive": list, "top_negative": list}, three factors each,
        ordered by impact.
    """
    raise NotImplementedError


def simulate_card_payoff(applicant: CreditApplicant, card_id: str) -> dict:
    """US-M3-02: Show how the score would change if one card was paid off.

    Args:
        applicant: The applicant to simulate for.
        card_id: ID of the credit card to pay off.

    Returns:
        {"current_score": int, "simulated_score": int, "change": int}
    """
    raise NotImplementedError


def format_score_history(score_history: list, months: int = 12) -> str:
    """US-M3-03: Show the applicant's score trend over the last 12 months.

    Text-based only (the brief allows no GUI), e.g. a text bar chart.

    Args:
        score_history: Past scores, newest first, as dicts with keys
            "month" and "score".
        months: How many months to show.

    Returns:
        The score history as a printable text chart.
    """
    raise NotImplementedError


def apply_weighting_profile(metrics_profile: dict,
                            profile_name: str) -> dict:
    """US-M3-04: Score the applicant using a chosen weighting profile.

    Args:
        metrics_profile: The profile from build_metrics_profile().
        profile_name: e.g. "Conservative" or "High Risk".

    Returns:
        {"score": int, "score_breakdown": dict, "profile": str}
    """
    weights_by_profile = {
        "Conservative": {"payment_history": 0.40, "dti": 0.35, "utilisation": 0.25},
        "High Risk": {"payment_history": 0.60, "dti": 0.25, "utilisation": 0.15},
    }
    if profile_name not in weights_by_profile:
        raise ValueError(f"Unknown weighting profile: {profile_name}")

    payment_score = metrics_profile["payment_history"]["consistency_score"]
    if payment_score is None:
        raise ValueError("Insufficient payment history")

    dti = metrics_profile["dti"]
    utilisation = metrics_profile["overall_utilisation"]["utilisation"]
    raw_metrics = {
        "payment_history": payment_score,
        "dti": dti,
        "utilisation": utilisation,
    }
    for name, value in raw_metrics.items():
        if type(value) not in (int, float) or not 0 <= value <= 100:
            raise ValueError(f"{name} must be a number between 0 and 100")

    factor_scores = {
        "payment_history": payment_score,
        "dti": 100 - dti,
        "utilisation": 100 - utilisation,
    }
    weights = weights_by_profile[profile_name]

    breakdown = {
        name: (value - 50) * weights[name] * 5.5
        for name, value in factor_scores.items()
    }
    return {
        "score": round(575 + sum(breakdown.values())),
        "score_breakdown": breakdown,
        "profile": profile_name,
    }


def check_score_drop_alert(score_history: list) -> str:
    """US-M3-05: Alert if the score fell by more than 20 points in a month.

    Args:
        score_history: Past scores, newest first.

    Returns:
        An alert message, or an empty string if there is no alert.
    """
    raise NotImplementedError


def compare_with_age_bracket(score: int, age: int,
                             all_applicants: list) -> dict:
    """US-M3-06: Compare the score with the average for the age bracket.

    Args:
        score: The applicant's credit score.
        age: The applicant's age.
        all_applicants: Every stored CreditApplicant with a score.

    Returns:
        {"age_bracket": str, "bracket_average": float, "difference": float}
    """
    raise NotImplementedError


def flag_score_caps(metrics_profile: dict, score: int) -> list:
    """US-M3-07: Flag when the score was capped by a severe negative metric.

    Args:
        metrics_profile: The profile from build_metrics_profile().
        score: The score before any caps.

    Returns:
        A list of flag messages explaining each cap applied.
    """
    raise NotImplementedError


def recalculate_score(applicant: CreditApplicant,
                      profile_name: str = "Standard") -> dict:
    """US-M3-08: Recalculate the score after the applicant's file changes.

    Args:
        applicant: The updated applicant.
        profile_name: The weighting profile to use.

    Returns:
        The new score result, as returned by apply_weighting_profile().
    """
    raise NotImplementedError


def generate_score_summary(score: int, factors: dict) -> str:
    """US-M3-09: Explain the score in plain English for the applicant.

    Args:
        score: The final credit score.
        factors: The result of rank_score_factors().

    Returns:
        A short plain-English summary of why the score is what it is.
    """
    raise NotImplementedError
