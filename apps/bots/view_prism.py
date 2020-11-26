import re
import requests
import traceback
from flask import request, jsonify, current_app
from utils.helper import RedPrint, ShareTokenAuth
from bases.globals import settings
from bases.exceptions import LogicError

api = RedPrint('api/v1/chatbot')


@api.route('/<path:uri>', methods=['GET', 'POST'])
def proxy_to_prism(uri):
    path = re.match('.*?(/api/v1/chatbot.*)', request.url).groups()
    path = path[0] if path else ''
    url = settings['PRISM_HOST'] + path
    headers = {i[0]: i[1] for i in request.headers}

    headers['Platform'] = settings['PRISM_PLATFORM']
    headers['Share-Token'] = ShareTokenAuth.encode(
        {
            'data': {'constant': settings['PRISM_CONSTANT']}
        },
        settings['PRISM_SECRET']
    )
    if request.method == 'GET':
        data = None
    else:
        data = request.json

    # request prism data
    try:
        res = requests.request(request.method, url, data=data, headers=headers)
        res_data = res.json()

        if res.status_code != 200:
            res_data['msg'] = res_data['err_msg']
        return jsonify(res_data), res.status_code
    except Exception:
        current_app.logger.error(traceback.format_exc())
        raise LogicError('未正确配置数据源。')

