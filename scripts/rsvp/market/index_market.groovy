response = [
    'type': 'card',
    'detail': 'IndexMarketList',
    'prefix_message': null,
    'jump_url': null,
    'quick_reply': [],
    'data': 主要指数行情
]

主要指数行情.each { key, value ->
    if (key != 'A股指数') {
        quick_reply_key = key + '基金'
        quick_reply_value = quick_reply_key + '有哪些？'
        response.quick_reply.add(['key': quick_reply_key, 'value': quick_reply_value])
    }
}