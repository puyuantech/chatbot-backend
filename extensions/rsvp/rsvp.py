import json
import time
import random
import hashlib
import requests


class Rsvp(object):

    def __init__(self, url, bot_id, share_token, logger=None):
        self.url = url
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

    def get_request_params(self, query, uid):
        data = {
            'botid': self.bot_id,
            'uid': uid,
            'q': query,
            'stage': 'release',
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

    def get_bot_response(self, query, uid):
        params = self.get_request_params(query, uid)
        resp = requests.get(self.url, headers=self.req_headers, params=params)
        # if self.logger:
        #     self.logger.info(f'url: {resp.request.url}')
        #     self.logger.info(f'headers: {resp.request.headers}')
        # else:
        #     print(f'url: {resp.request.url}')
        #     print(f'headers: {resp.request.headers}')
        resp = resp.json()
        if not resp or resp.get('status', 1) != 0 or not resp.get('stage'):
            import traceback
            if self.logger:
                self.logger.error(traceback.format_exc())
            else:
                print(traceback.format_exc())
            return None
        
        return resp
