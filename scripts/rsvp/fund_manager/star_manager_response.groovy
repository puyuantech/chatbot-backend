if (基金经理信息.size() == 1) {
    response_detail = 'FundManager'
    response_data = 基金经理信息[0]
} else {
    response_detail = 'FundManagerList'
    response_data = 基金经理信息
}

response = [
    'type': 'card',
    'detail': response_detail,
    'prefix_message': prefix_message,
    'jump_url': null,
    'quick_reply': quick_reply,
    'data': response_data
]