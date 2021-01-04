
from collections import defaultdict
from flask import request


def classify_by_fund_type(data):
    fund_infos = defaultdict(list)
    for fund_info in data:
        fund_infos[fund_info['基金类型']].append(fund_info)
    return fund_infos


def generate_fund_query_params():
    return {
        'page': int(request.args.get('page', 1)),
        'page_size': int(request.args.get('page_size', 10)),
        'ordering': request.args.get('ordering'),
    }

