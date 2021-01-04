
import functools

from flask import request

from ..constants import EMPTY_VALUE


def get_match_risk_level(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):

        match = request.json.get('match')
        risk_level = request.json.get('risk_level')
        if match in EMPTY_VALUE or risk_level in EMPTY_VALUE:
            self.input.risk_level = None
        else:
            self.input.risk_level = risk_level

        return func(self, *args, **kwargs)
    return wrapper

