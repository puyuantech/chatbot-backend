if (投资需求 == '安稳') {
    目标等级 = '安逸型'
} else if (投资需求 == '保守') {
    目标等级 = '保守型'
} else if (投资需求 == '稳健') {
    目标等级 = '稳健型'
} else if (投资需求 == '积极') {
    目标等级 = '积极型'
} else if (投资需求 == '进取' || 投资需求 == '激进') {
    目标等级 = '进取型'
} else {
    目标等级 = null
}

if ( !目标等级 ) {
    目标等级 = 风险承受能力
}

基金名称1 = '建信天添益A'
基金名称2 = '鹏华安盈宝'
prefix_message = null
jump_url = null

if (目标等级 == '保守型') {
    基金名称1 = '招商产业A'
    基金名称2 = '易方达丰和'
    jump_url = ['key': '点击查看详情', 'value': 'https://mp.weixin.qq.com/s/CcFRsGIzrJXynaeI3-nFlg']
    operation = 'set'
    tag_type = 'risk_tolerance'
    tag_value = 0.1

    prefix_message = '【大类配置-稳健】\n'
    prefix_message += '组合定位于稳健型风险偏好，希望通过大类配置的方式进行投资的投资者。\n'
    prefix_message += '\n'
    prefix_message += '预期年化收益：4%到6%\n'
    prefix_message += '预期最大回撤：5%以内\n'
    prefix_message += '推荐持有周期：半年以上\n'
    prefix_message += '\n'
    prefix_message += '我们的基本理念是大类资产配置，各种经济学、金融学经典理论还有多年的市场行情都表明，通过大类资产配置的方式，能够更具确定性地获取投资收益、控制投资风险，最终在长期投资的跑道上收获满意的成果。\n'
    prefix_message += '基于这样的诉求，棱镜研究院着手打造了固收增强组合，使用优选的债基+量化对冲基金作为收益打底，利用权益类资产与股债择时带来的收益进行收益增强，为大家的资产保值增值提供一个安心的避风港。\n'
    prefix_message += '\n'
    prefix_message += '放长线才能钓大鱼，根据回测历史数据，任意时间买入并持有1年，盈利概率为98.10%；持有3年，盈利概率为100%；持有5年，盈利概率为100%。\n'
} else if (目标等级 == '稳健型') {
    基金名称1 = '易方达裕丰回报'
    基金名称2 = '华夏鼎利A'
    jump_url = ['key': '点击查看详情', 'value': 'https://mp.weixin.qq.com/s/2a7Dbh82cMoZaAaNM0Zg3w']
    operation = 'set'
    tag_type = 'risk_tolerance'
    tag_value = 0.2

    prefix_message = '【固收增强组合】\n'
    prefix_message += '本组合定位于对固定收益资产进行一定程度的收益增强。\n'
    prefix_message += '\n'
    prefix_message += '预期年化收益：5%到7%\n'
    prefix_message += '预期最大回撤：小于5%\n'
    prefix_message += '推荐持有周期：半年以上\n'
    prefix_message += '\n'
    prefix_message += '习惯了投资传统固收类产品低风险又可以有较好收益的投资者，近年来越来越难找到自己满意的产品。\n'
    prefix_message += '基于这样的诉求，棱镜研究院着手打造了固收增强组合，使用优选的债基+量化对冲基金作为收益打底，利用权益类资产与股债择时带来的收益进行收益增强，为大家的资产保值增值提供一个安心的避风港。\n'
    prefix_message += '\n'
    prefix_message += '放长线才能钓大鱼，根据回测历史数据，任意时间买入并持有1年，盈利概率为87.50%；持有3年，盈利概率为99.72%；持有5年，盈利概率为100%。\n'
} else if (目标等级 == '积极型') {
    基金名称1 = '易方达安心回馈'
    基金名称2 = '泓德致远A'
    jump_url = ['key': '点击查看详情', 'value': 'https://mp.weixin.qq.com/s/fYq-Mb0oPl0CycjNrMg0pw']
    operation = 'set'
    tag_type = 'risk_tolerance'
    tag_value = 0.3

    prefix_message = '【大类配置-进取】\n'
    prefix_message += '本组合定位于进取型风险偏好，希望通过大类配置的方式进行投资的投资者。\n'
    prefix_message += '\n'
    prefix_message += '预期年化收益：8%到10%\n'
    prefix_message += '预期最大回撤：10%以内\n'
    prefix_message += '推荐持有周期：三年以上\n'
    prefix_message += '\n'
    prefix_message += '我们的基本理念是大类资产配置，各种经济学、金融学经典理论还有多年的市场行情都表明，通过大类资产配置的方式，能够更具确定性地获取投资收益、控制投资风险，最终在长期投资的跑道上收获满意的成果。'
    prefix_message += '\n'
    prefix_message += '放长线才能钓大鱼，根据回测历史数据，任意时间买入并持有1年，盈利概率为91.14%；持有3年，盈利概率为100%；持有5年，盈利概率为100%。\n'
} else if (目标等级 == '进取型') {
    基金名称1 = '易方达蓝筹精选'
    基金名称2 = '富国天惠精选成长A'
    jump_url = ['key': '点击查看详情', 'value': 'https://mp.weixin.qq.com/s/uCCP-oUR6OA1i-Z2q6l8hg']
    operation = 'set'
    tag_type = 'risk_tolerance'
    tag_value = 0.4

    prefix_message = '【时间机器】\n'
    prefix_message += '本组合定位于长期投资消费、医疗、科技三大未来赛道，通过优选基金经理和行业轮动进一步提升超额收益。\n'
    prefix_message += '\n'
    prefix_message += '预期年化收益：15%到25%\n'
    prefix_message += '预期最大回撤：50%以内\n'
    prefix_message += '推荐持有周期：十年以上\n'
    prefix_message += '\n'
    prefix_message += '精选出当前时点各赛道上三位优秀基金经理，形成最终九人组合。在此基础上，针对不同时期行业间的轮动进行一定程度的权重调整进一步增强收益。'
}

if ( prefix_message ) {
    推荐语 = '根据对您的风险承受能力的评估，为您推荐'
    if (目标等级 == '安逸型') {
        推荐语 += '以下两只优质货币基金。货币基金具有流动性高、风险低的特点。'
    } else if (目标等级 == '保守型') {
        推荐语 += '以下两只优质债券型基金和稳健组合。是收益稳定增值的好选择。'
    } else if (目标等级 == '稳健型') {
        推荐语 += '以下两只优质债券型基金和固收增强组合。使用债券类资产辅以少量优质权益类资产。'
    } else if (目标等级 == '积极型') {
        推荐语 += '以下两只优质偏债混合型基金和进取组合。使用债券类资产辅以大量优质权益类资产。'
    } else if (目标等级 == '进取型') {
        推荐语 += '以下两只优质股票型基金和时间机器组合。权益类产品可获得高收益的同时需要承受高风险。'
    } else {
        推荐语 += '以下两只优质货币基金。货币基金具有流动性高、风险低的特点。'
    }
    推荐语 += '\n点击下方「我的画像」可查看您的风险承受能力。\n'
    prefix_message = 推荐语 + prefix_message
} else {
    prefix_message = '小镜为您精选了以下产品。'
}

response = [
    'type': 'card',
    'detail': 'FundList',
    'prefix_message': prefix_message,
    'jump_url': jump_url,
    'quick_reply': [
        [
            'key': '满意',
            'value': '满意'
        ],
        [
            'key': '不满意',
            'value': '不满意'
        ]
    ],
    'data': []
]