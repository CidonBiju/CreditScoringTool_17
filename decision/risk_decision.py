"""Module 4 - Risk Assessment & Decisioning.

Owner: Cidon. User stories US-M4-01 to US-M4-09.

Turns the final credit score and metrics into a lending decision.
"""


def classify_risk_category(credit_score: int,
                           metrics_profile: dict) -> str:
    """US-M4-01: Classify the applicant into a lending risk category.

    Args:
        credit_score: Final credit score (300 to 850).
        metrics_profile: The profile from build_metrics_profile().

    Returns:
        The risk category, e.g. "Prime", "Near Prime", "Subprime" or
        "High Risk".
    """
    raise NotImplementedError


def validate_application(credit_score: int, loan_request: dict) -> list:
    """US-M4-02: Validate the score and loan application before assessment.

    Args:
        credit_score: Final credit score.
        loan_request: Dict with keys "amount", "term_months" and
            "purpose".

    Returns:
        A list of error messages; an empty list means the data is valid.
    """
    raise NotImplementedError


def requires_manual_review(credit_score: int, risk_category: str,
                           metrics_profile: dict,
                           loan_request: dict) -> tuple:
    """US-M4-03: Identify applications that need a manual review.

    Args:
        credit_score: Final credit score.
        risk_category: Result of classify_risk_category().
        metrics_profile: The profile from build_metrics_profile().
        loan_request: The loan request dict.

    Returns:
        (True/False, list of reasons for review)
    """
    raise NotImplementedError


def calculate_max_loan_amount(risk_category: str, monthly_income: float,
                              dti: float) -> float:
    """US-M4-04: Calculate the maximum recommended loan amount.

    Args:
        risk_category: Result of classify_risk_category().
        monthly_income: Gross monthly income in GBP.
        dti: Debt-to-Income ratio from Module 2 (0 to 100).

    Returns:
        The maximum recommended loan amount in GBP.
    """
    raise NotImplementedError


def recommend_interest_rate(risk_category: str, loan_amount: float,
                            term_months: int) -> float:
    """US-M4-05: Recommend an interest rate for the loan.

    Args:
        risk_category: Result of classify_risk_category().
        loan_amount: Requested loan amount in GBP.
        term_months: Loan term in months.

    Returns:
        The recommended annual interest rate as a percentage.
    """
    raise NotImplementedError


def assess_repayment_affordability(monthly_repayment: float,
                                   monthly_income: float,
                                   existing_commitments: float) -> dict:
    """US-M4-06: Check whether the monthly repayment is affordable.

    Args:
        monthly_repayment: Proposed monthly loan repayment in GBP.
        monthly_income: Gross monthly income in GBP.
        existing_commitments: Current monthly debt payments in GBP.

    Returns:
        {"affordable": bool, "repayment_ratio": float, "reason": str}
    """
    raise NotImplementedError


def assess_loan_request_suitability(requested_amount: float,
                                    max_loan_amount: float,
                                    affordability: dict) -> dict:
    """US-M4-07: Check the requested amount against limits and capacity.

    Args:
        requested_amount: Amount the applicant asked for in GBP.
        max_loan_amount: Result of calculate_max_loan_amount().
        affordability: Result of assess_repayment_affordability().

    Returns:
        {"suitable": bool, "suggested_amount": float or None,
         "reason": str}
    """
    raise NotImplementedError


def make_lending_decision(risk_category: str, affordability: dict,
                          suitability: dict, manual_review: tuple) -> str:
    """US-M4-08: Approve, reject or refer the loan application.

    Args:
        risk_category: Result of classify_risk_category().
        affordability: Result of assess_repayment_affordability().
        suitability: Result of assess_loan_request_suitability().
        manual_review: Result of requires_manual_review().

    Returns:
        "APPROVE", "REJECT" or "REFER".
    """
    raise NotImplementedError


def generate_decision_summary(decision: str, loan_terms: dict,
                              reasons: list) -> str:
    """US-M4-09: Produce a clear text summary of the lending decision.

    Args:
        decision: Result of make_lending_decision().
        loan_terms: Dict with keys "amount", "interest_rate" and
            "term_months".
        reasons: Reasons for the approval, rejection or referral.

    Returns:
        A readable multi-line summary of the decision.
    """
    raise NotImplementedError
