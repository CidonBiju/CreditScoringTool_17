# Credit Scoring Tool – CO3095 Group 17

A text-based credit scoring tool written in Python. It turns an applicant's
financial data into a credit score (300–850) and a lending decision.
There is no GUI and no database: applicant data is stored in a serialized
text file in `data/`.

## Team and modules

| Module | Code | Owner | User stories |
| --- | --- | --- | --- |
| 1. Data Ingestion & Storage | `ingestion/` | Ashvin | US-M1-01 to US-M1-09 |
| 2. Financial Metrics Engine | `metrics/financial_metrics.py` | Himesh | US-M2-01 to US-M2-09 |
| 3. Scoring Algorithm | `scoring/credit_scoring.py` | Gokul | US-M3-01 to US-M3-09 |
| 4. Risk Assessment & Decisioning | `decision/risk_decision.py` | Cidon | US-M4-01 to US-M4-09 |

Each user story is one function. Every function's docstring starts with
its user story ID, so code can be traced back to its GitHub issue.

## Project structure

```
credit_scoring_tool/
├── main.py                       # entry point
├── ingestion/                    # Module 1
│   ├── credit_applicant.py       # shared CreditApplicant data model
│   ├── applicant_input.py        # US-M1-01 to 04
│   ├── applicant_storage.py      # US-M1-05 to 08
│   └── menu.py                   # US-M1-09
├── metrics/financial_metrics.py  # Module 2
├── scoring/credit_scoring.py     # Module 3
├── decision/risk_decision.py     # Module 4
├── data/applicants.txt           # serialized applicant data
├── evidence/planning_poker/      # Planning Poker screenshots
└── <student_id>/test/            # each member's tests
    ├── blackbox/<technique>/
    └── whitebox/<technique>/
```

## Requirements

- Python 3.10 or newer (standard library only, nothing to install)
- PyCharm

## How to run

1. Unzip the submission and open PyCharm → **Open** → select the
   `credit_scoring_tool` folder.
2. Set the interpreter: bottom-right corner → **Add New Interpreter** →
   **Add Local Interpreter** → **Virtualenv** → **OK**.
3. Right-click `main.py` → **Run 'main'**, or in the PyCharm terminal run:
   `python main.py`

## How to run the tests

From the project root, in the PyCharm terminal:

```
python -m unittest discover -v
```

One member's tests only:

```
python -m unittest discover -s <student_id> -t . -v
```

Commands for each testing technique and for coverage will be added as the
tests are written.


