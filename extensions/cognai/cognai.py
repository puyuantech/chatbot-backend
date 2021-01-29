
import requests


class Cognai:

    def __init__(self, url, user_account, user_pwd):
        self.url = url
        self.user_account = user_account
        self.user_pwd = user_pwd
        self.token = None

    def get_response(self, q):
        '''
        获取对话结果
        '''
        if not self.token:
            self.token = self._get_token(self.user_account, self.user_pwd)
            if not self.token:
                return None

        params = {
            'q': q,
            'token': self.token
        }
        resp = requests.get(self.url + '/qa/finance_answer', params=params).json()
        return resp

    def _get_token(self, user_account, user_pwd):
        '''
        鉴权
        '''
        data = {
            'user_account': user_account,
            'user_pwd': user_pwd
        }

        headers = {
            'Content-Type': 'application/json'
        }
        resp = requests.post(self.url + '/user/get_token', headers=headers, json=data)

        resp = resp.json()
        if not resp or resp.get('code') != 0:
            return None
        return resp['data']['token']

