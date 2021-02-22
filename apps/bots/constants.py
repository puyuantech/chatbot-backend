
import json

from bases.base_enmu import EnumBase


EMPTY_VALUE = {None, '', 'null'}
MARKET_INDEX_IDS = {
    'sse_a': 'A股指数',
    'sse50': '上证50',
    'hs300': '沪深300',
    'csi500': '中证500',
    'gem': '创业板指',
    'hsi': '恒生指数',
    'sp500': '标普500',
    'nasdaq_100': '纳斯达克100',
}
ERROR_RSVP_RESPONSE = {
    'topic': 'fallback',
    'status': -1,
    'stage': [{
        'message': json.dumps({
            'text': {
                'type': 'message',
                'detail': 'error',
                'quick_reply': [],
                'data': '抱歉，刚才我没听懂，已经记下了。请问还有什么可以帮您？'
            },
        })
    }],
}


class Operation(EnumBase):
    set = 'set'
    update = 'update'


class TagType(EnumBase):
    expertise = 'expertise'
    risk_tolerance = 'risk_tolerance'


def get_bot_init_reply():
    return {
        'type': 'card',
        'detail': 'Swiper',
        'prefix_message': '您好，我是棱小镜，您的投资理财助理。您可以试试问我以下问题～\n如果您想了解我是谁，请',
        'jump_url': {'key': '点击查看', 'value': 'https://xj.prism-advisor.com/mini/intro?login=false'},
        'quick_reply': [
            {'key': '我要投资', 'value': '我要投资。'},
            {'key': '推荐基金', 'value': '给我推荐基金。'},
            {'key': '搜索基金', 'value': '我想搜索基金。'},
            {'key': '特色榜单', 'value': '我想看看特色榜单。'},
            {'key': '个性化推荐', 'value': '为我进行个性化推荐。'},
            {'key': '我的画像', 'value': '查看我的画像。'},
        ],
        'data': [
            {'title': '基金信息查询', 'items': [
                {'key': '汇添富经典成长怎么样？', 'value': '汇添富经典成长怎么样？'},
                {'key': '兴全趋势投资最近怎么样？', 'value': '兴全趋势投资最近怎么样？'},
                {'key': '汇添富创新医药的持仓有哪些？', 'value': '汇添富创新医药的持仓有哪些？'},
                {'key': '易方达张坤怎么样？', 'value': '易方达张坤怎么样？'},
                {'key': '劳杰男怎么样？', 'value': '劳杰男怎么样？'},
                {'key': '易方达中小盘的定投收益咋样？', 'value': '易方达中小盘的定投收益咋样？'},
                {'key': '易方达中小盘和银华中小盘精选哪个好？', 'value': '易方达中小盘和银华中小盘精选哪个好？'},
            ]},
            {'title': '基金推荐', 'items': [
                {'key': '明星基金经理有哪些？', 'value': '明星基金经理有哪些？'},
                {'key': '好的沪深300基金有哪些？', 'value': '好的沪深300基金有哪些？'},
                {'key': '消费基金有哪些？', 'value': '消费基金有哪些？'},
                {'key': '最近短线机会有哪些？', 'value': '最近短线机会有哪些？'},
                {'key': '中线机会有哪些？', 'value': '中线机会有哪些？'},
                {'key': '有哪些优秀的绝对收益基金？', 'value': '有哪些优秀的绝对收益基金？'},
                {'key': '哪些基金抗风险能力强？', 'value': '哪些基金抗风险能力强？'},
            ]},
            {'title': '市场行情', 'items': [
                {'key': '最近市场怎么样？', 'value': '最近市场怎么样？'},
                {'key': '最近有哪些热门板块？', 'value': '最近有哪些热门板块？'},
                {'key': '有哪些低估指数？', 'value': '有哪些低估指数？'},
                {'key': '云游戏概念股都有什么？', 'value': '云游戏概念股都有什么？'},
                {'key': '白酒行业营业收入前两名是谁？', 'value': '白酒行业营业收入前两名是谁？'},
                {'key': '贵州茅台的资产负债率怎么样？', 'value': '贵州茅台的资产负债率怎么样？'},
                {'key': '主营新能源电池的公司有哪些？', 'value': '主营新能源电池的公司有哪些？'},
            ]},
            {'title': '理财知识', 'items': [
                {'key': '科学投资理念(1)-坚持长期投资', 'value': 'https://mp.weixin.qq.com/s/gmj17EjwjeFBee5H0M4l0A'},
                {'key': '科学投资理念(2)-做好资产配置', 'value': 'https://mp.weixin.qq.com/s/Qt53mC1kN5WJ0jqXL0s98Q'},
                {'key': '科学投资理念(3)-明确能力边界', 'value': 'https://mp.weixin.qq.com/s/6i9q5xhjV3OQi19kxc3B1A'},
                {'key': '冷知识-基金ABCDEF...类份额', 'value': 'https://mp.weixin.qq.com/s/8UN5jQvFOGNOhQBBVYZwvA'},
                {'key': '基金组合应如何分类和筛选', 'value': 'https://mp.weixin.qq.com/s/LZ9yX9I5-X-C8blMXPKJ2A'},
                {'key': '应该定投还是趸投（一把梭）？', 'value': 'https://mp.weixin.qq.com/s/yptszZJ3zfQ-f9jhCjWeCw'},
                {'key': '冷知识-基金暴涨暴跌原因？', 'value': 'https://mp.weixin.qq.com/s/fvKHp0EwLwhRZOA-lOk4qg'},
            ]},
        ]
    }

