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
    'prefix_message': null,
    'jump_url': null,
    'quick_reply': [
        [
            'key': '我要投资',
            'value': '我要投资。'
        ],
        [
            'key': '推荐基金',
            'value': '给我推荐基金。'
        ],
        [
            'key': '搜索基金',
            'value': '我想搜索基金。'
        ],
        [
            'key': '特色榜单',
            'value': '我想看看特色榜单。'
        ],
        [
            'key': '个性化推荐',
            'value': '为我进行个性化推荐。'
        ],
        [
            'key': '个人画像',
            'value': '查看个人画像。'
        ]
    ],
    'data': response_data
]