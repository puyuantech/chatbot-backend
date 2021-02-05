profile = '您的画像：\n'
profile += '风险承受能力：' + 风险承受能力 + '\n'
profile += '投资经验程度：' + 投资经验程度 + '\n\n'
profile += '以上数据根据您的浏览记录生成，您可点击下方「风险测评」进行校准。'

response = [
    'type': 'message',
    'detail': 'text',
    'prefix_message': null,
    'jump_url': null,
    'quick_reply': [
        [
            'key': '个性化推荐',
            'value': '为我进行个性化推荐'
        ],
        [
            'key': '风险测评',
            'value': '我要进行风险测评。'
        ]
    ],
    'data': profile
]