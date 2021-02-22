response = [
    'type': 'card',
    'detail': 'FundHold',
    'prefix_message': 基金持仓.基金名称 + '的持仓如下：',
    'jump_url': null,
    'quick_reply': [
        [
            'key': '基金诊断',
            'value': 基金持仓.基金名称 + '怎么样'
        ],
        [
            'key': '最近涨幅',
            'value': 基金持仓.基金名称 + '最近涨幅如何？'
        ]
    ],
    'data': 基金持仓
]

基金名称 = null
基金代码 = null
查询持仓 = null
时间周期 = null
查询行情 = null