from flask import request
from utils.helper import RedPrint

api = RedPrint('bots')


@api.route('/example', methods=['GET'])
def example():
    print(request.endpoint)
    import time
    time.sleep(10)
    return 'example'


@api.route('/example2', methods=['GET'])
def example2():
    print(request.endpoint)
    import requests
    requests.get('http://127.0.0.1:8003/api/v1/bots/example')
    return 'example2'

