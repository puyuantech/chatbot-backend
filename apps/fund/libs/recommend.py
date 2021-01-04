
from ..constants import EMPTY_VALUE


def get_match_risk_level(match, risk_level):
    if match in EMPTY_VALUE or risk_level in EMPTY_VALUE:
        return None
    else:
        return risk_level

