if (时间周期 || 查询行情) {
    // 查询基金行情
    response = [
        'type': 'card',
        'detail': 'FundProfit',
        'prefix_message': null,
        'jump_url': null,
        'quick_reply': [
            [
                'key': '基金诊断',
                'value': 基金信息.基金名称 + '怎么样？'
            ],
            [
                'key': 基金信息.基金经理,
                'value': 基金信息.基金经理 + '怎么样？'
            ],
            [
                'key': '基金比较',
                'value': '我想对比基金。'
            ],
            [
                'key': '定投计算',
                'value': '该基金的定投表现怎么样？'
            ],
            [
                'key': '查看持仓',
                'value': 基金信息.基金名称 + '持仓有什么？'
            ],
            [
                'key': '什么是最大回撤？',
                'value': '什么是最大回撤？'
            ],
            [
                'key': '什么是年化收益？',
                'value': '什么是年化收益？'
            ]
        ],
        'data': 基金信息
    ]
} else {
    // 查询基金详情
    prefix_message = '小镜提示您：'

    if (基金信息.基金类型 == '股票型') {
        prefix_message += "股票型基金需要较好的风险承受能力。"
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

    if (风险承受能力 == '高') {
        self_risk_level = 5;
    } else if (风险承受能力 == '较高') {
        self_risk_level = 4;
    } else if (风险承受能力 == '中') {
        self_risk_level = 3;
    } else if (风险承受能力 == '较低') {
        self_risk_level = 2;
    } else {
        self_risk_level = 1;
    }

    if (基金信息.风险等级 == 'R5') {
        fund_risk_level = 5;
    } else if (基金信息.风险等级 == 'R4') {
        fund_risk_level = 4;
    } else if (基金信息.风险等级 == 'R3') {
        fund_risk_level = 3;
    } else if (基金信息.风险等级 == 'R2') {
        fund_risk_level = 2;
    } else {
        fund_risk_level = 1;
    }

    if (self_risk_level < fund_risk_level) {
        prefix_message += "当前基金的风险超过您的风险承受能力，请谨慎操作!"
    } else  {
        prefix_message += "投资有风险，入市须谨慎～"
    }

    response = [
        'type': 'card',
        'detail': 'FundBase',
        'prefix_message': prefix_message,
        'jump_url': null,
        'quick_reply': [
            [
                'key': 基金信息.基金经理,
                'value': 基金信息.基金经理 + '怎么样？'
            ],
            [
                'key': '基金比较',
                'value': '我想对比基金。'
            ],
            [
                'key': '定投计算',
                'value': '该基金的定投表现怎么样？'
            ],
            [
                'key': '最近涨幅',
                'value': 基金信息.基金名称 + '最近涨幅如何？'
            ],
            [
                'key': '查看持仓',
                'value': 基金信息.基金名称 + '持仓有什么？'
            ],
            [
                'key': '什么是最大回撤？',
                'value': '什么是最大回撤？'
            ],
            [
                'key': '什么是年化收益？',
                'value': '什么是年化收益？'
            ]
        ],
        'data': 基金信息
    ]
}

基金名称 = null
基金代码 = null
查询持仓 = null
时间周期 = null
查询行情 = null