
from ..constants import EMPTY_VALUE


def get_match_risk_level(match, risk_level):
    if match not in EMPTY_VALUE and risk_level not in EMPTY_VALUE:
        return risk_level

