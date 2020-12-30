
from bases.base_enmu import EnumBase


class PoolType(EnumBase):
    精选 = 'basic'
    新星 = 'new'
    老司机 = 'old'


class RecommendFundType(EnumBase):
    股票 = 'stock'
    债券 = 'bond'
    指数 = 'index'
    QDII = 'QDII'
    货币 = 'mmf'

