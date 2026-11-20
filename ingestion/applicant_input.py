"""Module 1 - Data Ingestion & Storage: text-based input and validation.

Owner: Ashvin. User stories US-M1-01 to US-M1-04.
"""

from ingestion.credit_applicant import CreditApplicant


def create_applicant_profile(existing_ids: list) -> CreditApplicant:
    """US-M1-01: Capture a new applicant's name, ID and age via text prompts.

    Handles format checking, duplicate ID prevention and retry/fallback
    when the user enters invalid values.

    Args:
        existing_ids: IDs already used, to prevent duplicates.

    Returns:
        A new CreditApplicant with name, ID and age filled in.
    """
    raise NotImplementedError


def validate_personal_info(name: str, applicant_id: str, age: int) -> list:
    """US-M1-02: Validate personal information with multiple rules.

    Checks age boundaries, string length limits, illegal characters and
    the applicant ID pattern.

    Args:
        name: Applicant's full name.
        applicant_id: Applicant ID to check.
        age: Age in whole years.

    Returns:
        A list of error messages; an empty list means the data is valid.
    """
    raise NotImplementedError


def input_financial_data() -> dict:
    """US-M1-03: Collect debts, incomes and credit limits in a text loop.

    Converts typed text to numbers in real time and re-prompts on
    conversion errors until the user finishes.

    Returns:
        A dict of the entered financial data.
    """
    raise NotImplementedError


def validate_financial_data(financial_data: dict) -> list:
    """US-M1-04: Validate all financial inputs.

    Rejects negative values, missing fields, unrealistic amounts and
    values that cannot be parsed as numbers.

    Args:
        financial_data: The dict returned by input_financial_data().

    Returns:
        A list of error messages; an empty list means the data is valid.
    """
    raise NotImplementedError
