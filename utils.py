# finaTSE/utils.py

def clean_number(val: str) -> float:
    """Remove commas and convert to float. Handles '0' and empty strings."""
    if not val or val == "0":
        return 0.0
    return float(val.replace(",", ""))
