if (行业板块) {
    response_detail = 'SectorInfo'
    prefix_message = '以下是' + 行业板块 + '近期涨幅：'
    response_data = 板块行情[0]
} else {
    response_detail = 'SectorList'
    prefix_message = '寻找热门板块，跟随趋势，赚取短期收益。'
    response_data = 板块行情
}

response = [
    'type': 'card',
    'detail': response_detail,
    'prefix_message': prefix_message,
    'jump_url': ['key': '查看全部板块', 'value': 板块列表链接],
    'quick_reply': [],
    'data': response_data
]

板块行情.eachWithIndex { item, index ->
    if (index >= 5) return

    quick_reply_key = item.板块名称 + '基金'
    quick_reply_value = quick_reply_key + '有哪些？'
    response.quick_reply.add(['key': quick_reply_key, 'value': quick_reply_value])
}

response.quick_reply.add(['key': '中线机会', 'value': '最近的中线机会有哪些？'])
response.quick_reply.add(['key': '明星基金经理为我掌舵', 'value': '明星基金经理有哪些？'])