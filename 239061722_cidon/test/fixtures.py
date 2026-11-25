"""Build synthetic data in the agreed Module 2 profile format."""


def profile(dti=20, utilisation=30, severe_events=0):
    return {
        "dti": dti,
        "overall_utilisation": {"utilisation": utilisation},
        "payment_history": {"severe_events": severe_events},
    }
