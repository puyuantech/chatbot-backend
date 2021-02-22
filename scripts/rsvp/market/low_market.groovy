response = [
    'type': 'card',
    'detail': 'IndexList',
    'prefix_message': '以下是目前精选低估指数，您可以布局估值洼地，等待价值回归，做一个价值投资者。',
    'jump_url': ['key': '查看全部指数', 'value': 指数列表链接],
    'quick_reply': [],
    'data': ['PE低估指数': PE低估指数, 'PB低估指数': PB低估指数]
]

PE低估指数.each { item ->
    quick_reply_key = item.指数名称 + '基金'
    quick_reply_value = quick_reply_key + '有哪些？'
    response.quick_reply.add(['key': quick_reply_key, 'value': quick_reply_value])
}

PB低估指数.each { item ->
    quick_reply_key = item.指数名称 + '基金'
    quick_reply_value = quick_reply_key + '有哪些？'
    response.quick_reply.add(['key': quick_reply_key, 'value': quick_reply_value])
}

response.quick_reply.add(['key': '短线机会', 'value': '最近的短线机会有哪些？'])
response.quick_reply.add(['key': '明星基金经理为我掌舵', 'value': '明星基金经理有哪些？'])