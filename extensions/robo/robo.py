
import requests

from typing import List

from bases.globals import settings


class Robo:

    host = settings['PRISM_HOST']

    @staticmethod
    def _parse_result(result):
        if result['err_msg'] is not None:
            raise Exception()
        return result['data']

    @classmethod
    def _request_get(cls, endpoint, data=None):
        response = requests.get(cls.host + endpoint, params=data)
        return cls._parse_result(response.json())

    @classmethod
    def _request_post(cls, endpoint, data=None):
        response = requests.post(cls.host + endpoint, json=data)
        return cls._parse_result(response.json())

    @classmethod
    def get_fund_info(cls, fund_ids, user_id=None) -> List[dict]:
        if not fund_ids:
            return []

        endpoint = '/api/v1/robo/fund/info'
        data = {
            'fund_ids': fund_ids,
            'user_id': user_id,
        }
        return cls._request_post(endpoint, data)

    @classmethod
    def get_fund_types(cls, fund_ids) -> dict:
        if not fund_ids:
            return {'股票型': 0, '指数型': 0}

        endpoint = '/api/v1/robo/fund/types'
        data = {
            'fund_ids': fund_ids,
        }
        return cls._request_post(endpoint, data)

    @classmethod
    def get_index_list(cls) -> List[str]:
        endpoint = '/api/v1/robo/index/list'
        return cls._request_get(endpoint)

