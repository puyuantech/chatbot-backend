
import logging
import requests

from bases.globals import settings
from urllib.parse import quote


class UrlManager:

    logger = logging.getLogger('UrlManager')
    url = 'http://api.3w.cn/api.htm?format=json&domain=1&url={}&key=' + settings['SHORT_URL_KEY']

    @classmethod
    def generate_short_url(cls, long_url, permanent=False):
        '''
        permanent: Expires in three months if false else Never expires
        '''
        request_url = cls.url.format(quote(long_url))
        if permanent:
            request_url += '&expireDate=2040-01-01'

        response = requests.get(request_url).json()
        if response['code'] == '1':
            cls.logger.error(f"[generate_short_url] (err_msg){response['err']} (long_url){long_url} (short_url){response['url']}")
            return

        cls.logger.info(f"[generate_short_url] (long_url){long_url} (short_url){response['url']}")
        return response['url']

