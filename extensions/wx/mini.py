
import json
import requests

from utils.crypt import WXBizDataCrypt
from bases.globals import settings


class WXUnion:

    # wx, web (app_id, app_secret, code)
    ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret=' \
                       '{}&code={}&grant_type=authorization_code'
    # (access_token, open_id)
    USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}'
    # mini (app_id, app_secret, code)
    MINI_URL = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}' \
               '&grant_type=authorization_code'

    @staticmethod
    def request(url):
        response = requests.get(url, timeout=3)
        return json.loads(response.content)

    @staticmethod
    def decode_union_id(session_key, iv, encrypted_data, mp_app_id):
        wx_crypt = WXBizDataCrypt(mp_app_id, session_key)
        decoded_data = wx_crypt.decrypt(encrypted_data, iv)
        return decoded_data.get('unionId')

    @classmethod
    def get_union_id_by_mini(cls, app_id, app_secret, code, iv, encrypted_data):
        content = cls.request(cls.MINI_URL.format(app_id, app_secret, code))
        if content.get('errcode'):
            raise Exception('[get_union_id_by_mini] failed to get union_id (errcode){} (errmsg){}'.format(content.get('errcode'), content.get('errmsg')))

        if 'unionid' not in content and 'session_key' in content:
            content['unionid'] = cls.decode_union_id(content.get('session_key'), iv, encrypted_data, app_id)

        assert content.get('unionid'), '[get_union_id_by_mini] failed to get union_id (errcode){} (errmsg){}'.format(content.get('errcode'), content.get('errmsg'))
        return content

    @classmethod
    def get_union_id_by_token(cls, app_id, app_secret, code):
        content = cls.request(cls.ACCESS_TOKEN_URL.format(app_id, app_secret, code))
        if content.get('errcode'):
            raise Exception('[get_union_id_by_token] failed to get access_token (errcode){} (errmsg){}'.format(content.get('errcode'), content.get('errmsg')))

        content = cls.request(cls.USER_INFO_URL.format(content['access_token'], content['openid']))
        if content.get('errcode'):
            raise Exception('[get_union_id_by_token] failed to get user_info (errcode){} (errmsg){}'.format(content.get('errcode'), content.get('errmsg')))

        assert content.get('unionid'), '[get_union_id_by_token] failed to get union_id (errcode){} (errmsg){}'.format(content.get('errcode'), content.get('errmsg'))
        return content

    def get_union_id(self, app_name, *params):
        assert 'WX' in settings, f'could not find "WX" setting in wechat apps config'
        config = settings['WX']

        assert app_name in config, f'could not find "{app_name}" setting in wechat apps config'
        app_type = config[app_name]['type']
        assert app_type in ('official', 'web', 'mini'), f'could not parse "{app_type}" as wechat app type'

        app_id, app_secret = config[app_name]['app_id'], config[app_name]['app_secret']
        if app_type == 'mini':
            return WXUnion.get_union_id_by_mini(app_id, app_secret, *params)
        else:
            return WXUnion.get_union_id_by_token(app_id, app_secret, *params)
