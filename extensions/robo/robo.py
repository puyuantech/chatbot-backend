
import requests

from typing import List

from bases.globals import settings


class Robo:

    host: str = settings['PRISM_HOST']

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
    def get_fund_manager_info(cls, manager_ids, user_id=None) -> List[dict]:
        if not manager_ids:
            return []

        endpoint = '/api/v1/robo/fund/manager'
        data = {
            'manager_ids': manager_ids,
            'user_id': user_id,
        }
        return cls._request_post(endpoint, data)

    @classmethod
    def get_fund_by_pagination(cls, fund_ids, user_id, fund_type, page, page_size, ordering) -> List[dict]:
        endpoint = '/api/v1/robo/fund/pagination'
        data = {
            'fund_ids': fund_ids,
            'user_id': user_id,
            'fund_type': fund_type,
            'page': page,
            'page_size': page_size,
            'ordering': ordering,
        }
        return cls._request_post(endpoint, data)

    @classmethod
    def get_fund_by_recommend(cls, fund_ids, user_id, risk_level, ordering=None, filters=None, contains=None) -> dict:
        endpoint = '/api/v1/robo/fund/recommend'
        data = {
            'fund_ids': fund_ids,
            'user_id': user_id,
            'risk_level': risk_level,
            'ordering': ordering,
            'filters': filters,
            'contains': contains,
        }
        return cls._request_post(endpoint, data)

    @classmethod
    def get_fund_by_recommend_xirr(cls, fund_ids, user_id, risk_level, init_bench, amt_bench, tot_mv, periods) -> dict:
        endpoint = '/api/v1/robo/fund/recommend/xirr'
        data = {
            'fund_ids': fund_ids,
            'user_id': user_id,
            'risk_level': risk_level,
            'init_bench': init_bench,
            'amt_bench': amt_bench,
            'tot_mv': tot_mv,
            'periods': periods,
        }
        return cls._request_post(endpoint, data)

    @classmethod
    def get_fund_by_recommend_risk_income(cls, fund_ids, user_id, risk_level, min_income, max_income, min_risk, max_risk) -> dict:
        endpoint = '/api/v1/robo/fund/recommend/risk_income'
        data = {
            'fund_ids': fund_ids,
            'user_id': user_id,
            'risk_level': risk_level,
            'min_income': min_income,
            'max_income': max_income,
            'min_risk': min_risk,
            'max_risk': max_risk,
        }
        return cls._request_post(endpoint, data)

    @classmethod
    def get_fund_by_recommend_hold_stock(cls, fund_ids, user_id, stock_name) -> dict:
        endpoint = '/api/v1/robo/fund/recommend/hold_stock'
        data = {
            'fund_ids': fund_ids,
            'user_id': user_id,
            'stock_name': stock_name,
        }
        return cls._request_post(endpoint, data)

    @classmethod
    def get_fund_by_recommend_hold_bond(cls, fund_ids, user_id, bond_name) -> dict:
        endpoint = '/api/v1/robo/fund/recommend/hold_bond'
        data = {
            'fund_ids': fund_ids,
            'user_id': user_id,
            'bond_name': bond_name,
        }
        return cls._request_post(endpoint, data)

    @classmethod
    def get_fund_by_recommend_etf(cls, user_id, index, etf_type) -> dict:
        endpoint = '/api/v1/robo/fund/recommend/etf'
        data = {
            'user_id': user_id,
            'index': index,
            'etf_type': etf_type,
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
    def get_index_list(cls) -> dict:
        endpoint = '/api/v1/robo/index/list'
        return cls._request_get(endpoint)

