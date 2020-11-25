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


class Operation(EnumBase):
    set = 'set'
    update = 'update'

