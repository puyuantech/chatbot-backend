prefix_message = '小镜提示您：'

if (基金信息.基金类型 == '股票型') {
    prefix_message += "股票型基金需要较好的风险承受能力哦，请您投资前了解自己的风险承受能力。"
} else if (基金信息.基金类型 == '货币型') {
    prefix_message += "货币基金风险低，同时收益也不高，但是流动性高，有些货币基金T+0赎回，随用随取，您可以将准备6-12个月的零花钱放在货币基金中，以备不时之需的同时还能赚点收益哦～"
} else if (基金信息.基金类型 == '债券型') {
    prefix_message += "债券基金风险低，波动小，不需要择时，适合趸投，与股票型基金相关性低，可以用来进行资产配置。"
} else if (基金信息.基金类型 == '指数型') {
    prefix_message += "债券基金风险低指数型基金跟踪标的，指数的构成具有优胜劣汰的优点，投资指数型基金省心省力，是个不错的选择哦。"
} else if (基金信息.基金类型 == 'QDII型') {
    prefix_message += "QDII基金投资海外资产，是您布局全球的好帮手。"
} else {
    prefix_message += "您说什么？我没听懂。"
}

response = [
    'type': 'card',
    'detail': 'FundBase',
    'prefix_message': prefix_message,
    'jump_url': ['key': 基金信息.基金名称 + '定投计算器', 'value': 基金信息.基金定投链接],
    'quick_reply': [],
    'data': 基金信息
]