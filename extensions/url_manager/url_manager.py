
import logging
import requests

from bases.globals import settings


class UrlManager:

    logger = logging.getLogger('UrlManager')
    request_url = 'https://ljxj.top/yourls-api.php'

    @classmethod
    def generate_short_url(cls, long_url, permanent=False):
        '''
        permanent: Expires in three months if false else Never expires
        '''
        params = {
            'url': long_url,
            'action': 'shorturl',
            'format': 'json',
            'signature': settings['SHORT_URL_KEY']
        }

        response = requests.get(cls.request_url, params=params).json()
        if response['statusCode'] != 200:
            cls.logger.error(f"[generate_short_url] (statusCode){response['statusCode']} "
                f"(status){response['status']} (message){response['message']}")
            return None

        cls.logger.info(f"[generate_short_url] (long_url){long_url} (short_url){response['shorturl']}")
        return response['shorturl']
