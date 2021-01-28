
from bases.globals import settings

from .cognai import Cognai


class CognaiBot:

    cognai_conf = settings['THIRD_SETTING']['cognai']

    @classmethod
    def get_cognai_bot(cls):
        return Cognai(cls.cognai_conf['url'], cls.cognai_conf['user_account'], cls.cognai_conf['user_pwd'])

