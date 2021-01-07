import json
import time
import random
import hashlib
import requests

from urllib import parse
from extensions.segmentation import Segmentation


class Rsvp(object):

    def __init__(self, url, bot_id, share_token, logger=None):
        self.chat_url = parse.urljoin(url, 'sandbox/chat')
        self.bot_info_url = parse.urljoin(url, 'server/api/botinfo')
        self.bot_id = bot_id
        self.req_headers = {
            'Content-Type': 'application/json',
            'x-share-token': share_token
        }
        self.logger = logger

    def get_nonce(self):
        '''
        生成一个随机1到8位长度的随机字符串
        '''
        base_str = list('ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789')
        length = random.randint(20, 20)
        samples = random.sample(base_str, length)
        return ''.join(samples)

    def get_sign(self, data):
        '''
        计算sign
        '''
        json_dict = dict()
        json_dict.update(data)
        json_str = json.dumps(json_dict, sort_keys=True)
        m = hashlib.md5() 
        m.update(json_str.encode()) 
        return m.hexdigest()

    def get_request_params(self, query, uid, stage):
        data = {
            'botid': self.bot_id,
            'uid': uid,
            'q': query,
            'stage': stage,
            'nonce': self.get_nonce(),
            'timestamp': int(time.time())
        }
        sign = self.get_sign(data) 
        data.update({'sign': sign})

        # if self.logger:
        #     self.logger.info(f'data: {data}')
        # else:
        #     print(f'data: {data}')

        return data

    def get_bot_response(self, query, uid, stage='release', final=False):
        params = self.get_request_params(query, uid, stage)
        resp = requests.get(self.chat_url, headers=self.req_headers, params=params)
        # if self.logger:
        #     self.logger.info(f'url: {resp.request.url}')
        #     self.logger.info(f'headers: {resp.request.headers}')
        # else:
        #     print(f'url: {resp.request.url}')
        #     print(f'headers: {resp.request.headers}')
        resp = resp.json()

        # if not final:
        #     if (not resp or resp.get('status', 1) != 0 or not resp.get('stage') 
        #             or resp.get('topic', 'fallback') == 'fallback'):
        #         segmentation = Segmentation()
        #         candidates = segmentation.match(query)
        #         if candidates:
        #             return self.get_bot_response(candidates[0], query, uid, stage, final=True)

        if not resp or resp.get('status', 1) != 0 or not resp.get('stage'):
            if self.logger:
                self.logger.error(f'Fail to parse bot resp: {resp}')
            else:
                print(f'Fail to parse bot resp: {resp}')
            return None

        return resp

    def get_bot_info(self):
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'botId': self.bot_id
        }
        resp = requests.get(self.bot_info_url, headers=headers, params=params)
        return resp.json()
