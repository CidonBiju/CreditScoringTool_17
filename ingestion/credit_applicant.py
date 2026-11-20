"""Shared data model: the CreditApplicant class used by every module.

Owner: Ashvin (Module 1). Other modules read these attributes, so any
change to an attribute name must be agreed with the whole group.
"""


class CreditApplicant:
    """One loan applicant and all of their financial data.

    Attributes:
        applicant_id: Unique applicant ID.
        name: Applicant's full name.
        age: Age in whole years.
        monthly_income: Gross monthly income in GBP.
        income_type: "salaried", "contract" or "self_employed".
        housing_payment: Monthly rent or mortgage payment in GBP.
        loan_payments: Total monthly loan payments in GBP.
        card_balance: Total credit card balance in GBP.
        card_min_payment: Monthly credit card minimum payment in GBP.
        accounts: List of account dicts with keys "id", "type",
            "balance", "limit", "status", "opened" and "closed".
        payment_records: List of payment status codes, newest month first
            (ON_TIME, LATE_30, LATE_60, LATE_90, MISSED, DEFAULT,
            NO_PAYMENT_DUE).
        public_records: List of dicts with keys "type", "date",
            "satisfied" and "discharged".
        searches: List of credit search dicts with keys "date" and "kind".
        score_history: List of past scores, newest first, as dicts with
            keys "month" (e.g. "2026-11") and "score".
    """

    def __init__(self, applicant_id: str, name: str, age: int,
                 monthly_income: float = 0.0,
                 income_type: str = "salaried",
                 housing_payment: float = 0.0,
                 loan_payments: float = 0.0,
                 card_balance: float = 0.0,
                 card_min_payment: float = 0.0,
                 accounts: list = None,
                 payment_records: list = None,
                 public_records: list = None,
                 searches: list = None,
                 score_history: list = None) -> None:
        self.applicant_id = applicant_id
        self.name = name
        self.age = age
        self.monthly_income = monthly_income
        self.income_type = income_type
        self.housing_payment = housing_payment
        self.loan_payments = loan_payments
        self.card_balance = card_balance
        self.card_min_payment = card_min_payment
        self.accounts = accounts if accounts is not None else []
        self.payment_records = (payment_records
                                if payment_records is not None else [])
        self.public_records = (public_records
                               if public_records is not None else [])
        self.searches = searches if searches is not None else []
        self.score_history = (score_history
                              if score_history is not None else [])
