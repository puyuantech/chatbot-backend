
from flask import current_app

from bases.globals import settings

from .rsvp import Rsvp


rsvp_conf = settings['THIRD_SETTING']['rsvp']


class RsvpBot:

    @staticmethod
    def get_rsvp_bot(bot_id=rsvp_conf['bot_id'], share_token=rsvp_conf['share_token']):
        return Rsvp(rsvp_conf['url'], bot_id, share_token, current_app.logger)

