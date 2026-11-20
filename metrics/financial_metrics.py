"""Module 2 - Financial Metrics Engine.

Owner: Himesh. User stories US-M2-01 to US-M2-09.

Turns an applicant's raw financial data into clean metrics that the
scoring module (Module 3) uses. Every function is pure: no input() or
print(), and invalid input raises ValueError.

Units used by every function:
    - percentages are floats from 0 to 100, rounded to 2 decimal places
    - ages and time spans are whole months
    - dates are datetime.date objects, and "today" is always passed in

Payment status codes: ON_TIME, LATE_30, LATE_60, LATE_90, MISSED,
DEFAULT, NO_PAYMENT_DUE.
"""

from datetime import date

from ingestion.credit_applicant import CreditApplicant


# ---------------------------------------------------------------------------
# Sprint 1
# ---------------------------------------------------------------------------

def calculate_dti(monthly_income: float, income_type: str,
                  housing_payment: float, loan_payments: float,
                  card_balance: float, card_min_payment: float) -> float:
    """US-M2-01: Calculate the applicant's Debt-to-Income ratio.

    Args:
        monthly_income: Gross monthly income in GBP (must be > 0).
        income_type: "salaried", "contract" or "self_employed".
        housing_payment: Monthly rent or mortgage payment.
        loan_payments: Total monthly loan payments.
        card_balance: Total credit card balance.
        card_min_payment: Monthly card minimum payment (0 if unknown).

    Returns:
        DTI as a percentage from 0 to 100, rounded to 2 decimal places.

    Raises:
        ValueError: If income is not positive, a debt value is negative
            or the income type is unknown.
    """
    raise NotImplementedError


def calculate_overall_utilisation(accounts: list) -> dict:
    """US-M2-02: Calculate overall credit utilisation of revolving accounts.

    Args:
        accounts: List of account dicts with keys "id", "type",
            "balance", "limit" and "status".

    Returns:
        {"utilisation": float or None, "over_limit_accounts": int}

    Raises:
        ValueError: If revolving accounts exist but all have invalid limits.
    """
    raise NotImplementedError


def evaluate_payment_history(payment_records: list) -> dict:
    """US-M2-04: Score payment consistency, weighting recent months more.

    Args:
        payment_records: List of payment status codes, newest month first.

    Returns:
        {"consistency_score": float or None, "severe_events": int}

    Raises:
        ValueError: If a record is not a known payment status code.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Sprint 2
# ---------------------------------------------------------------------------

def calculate_credit_history_age(accounts: list, today: date) -> dict:
    """US-M2-03: Calculate oldest and average account age.

    Args:
        accounts: List of account dicts with keys "opened" and "closed".
        today: The date to measure ages from.

    Returns:
        {"oldest_months": int, "average_months": float, "thin_file": bool}

    Raises:
        ValueError: If an account opens after today or closes before it
            opened.
    """
    raise NotImplementedError


def analyse_card_utilisation(cards: list) -> dict:
    """US-M2-05: Check each card's utilisation and find the worst card.

    Args:
        cards: List of card dicts with keys "id", "balance", "limit"
            and "status".

    Returns:
        {"highest_pct", "highest_card_id", "cards_over_30",
         "cards_over_75", "over_limit", "single_card_maxed"}
    """
    raise NotImplementedError


def detect_delinquency_patterns(payment_records: list) -> dict:
    """US-M2-06: Detect late-payment streaks and recent delinquency.

    Args:
        payment_records: List of payment status codes, newest month first.

    Returns:
        {"longest_late_streak": int, "months_since_last_late": int or None,
         "recovered": bool, "repeat_serious": bool}

    Raises:
        ValueError: If a record is not a known payment status code.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Sprint 3
# ---------------------------------------------------------------------------

def assess_negative_records(public_records: list, today: date) -> dict:
    """US-M2-07: Count and rank CCJs, defaults, IVAs and bankruptcies.

    Records 72 or more months old are ignored (UK 6-year rule).

    Args:
        public_records: List of dicts with keys "type", "date",
            "satisfied" and "discharged".
        today: The date to measure record ages from.

    Returns:
        {"active_count": int, "max_severity": int,
         "most_severe_label": str or None,
         "months_since_most_recent": int or None}

    Raises:
        ValueError: If a record is dated after today or has an unknown type.
    """
    raise NotImplementedError


def calculate_recent_credit_activity(searches: list, accounts: list,
                                     today: date) -> dict:
    """US-M2-08: Count recent hard searches and newly opened accounts.

    Hard searches within 14 days of each other count once (rate shopping).

    Args:
        searches: List of dicts with keys "date" and "kind" (hard/soft).
        accounts: List of account dicts with key "opened".
        today: The date to measure from.

    Returns:
        {"hard_searches_6m": int, "hard_searches_12m": int,
         "new_accounts_6m": int}

    Raises:
        ValueError: If a search has an unknown kind or a future date.
    """
    raise NotImplementedError


def build_metrics_profile(applicant: CreditApplicant, today: date) -> dict:
    """US-M2-09: Build one profile containing every Module 2 metric.

    Missing or invalid sections never crash the profile; they are
    recorded in "data_issues" instead.

    Args:
        applicant: The applicant to measure.
        today: The date to measure from.

    Returns:
        All metric results plus {"completeness": str,
        "data_issues": list, "thin_file": bool}.

    Raises:
        ValueError: If applicant is None.
    """
    raise NotImplementedError
