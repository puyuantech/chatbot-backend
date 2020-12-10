
import json
import requests

from bases.globals import settings

class WxWorkNotification(object):

    def __init__(self, logger=None):
        self.webhook_url = settings['BAD_CASE_REPORTER']
        self.logger = logger

    def send(self, content):
        message = {
            'msgtype': 'text',
            'text': {
                'content': content
            }
        }

        try:
            rsp = requests.post(self.webhook_url, json=message, timeout=3)
            data = json.loads(rsp.text)

            if data['errcode'] == 45009:
                self.logger.warning('[Wxwork] api freq out of limit (err_msg){}'.format(data['errmsg']))
            else:
                self.logger.error('[Wxwork] unknown rsp (rsp){}'.format(data))
        except Exception as e:
            self.logger.error('[Wxwork] exception (err_msg){}'.format(e))
