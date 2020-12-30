
from flask import request


def generate_fund_query_params():
    return {
        'page': int(request.args.get('page', 1)),
        'page_size': int(request.args.get('page_size', 10)),
        'ordering': request.args.get('ordering'),
    }

