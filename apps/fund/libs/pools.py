
import functools

from bases.exceptions import ParamsError

from ..constants import PoolType


def check_pool_type_valid(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):

        if self.input.pool_type not in PoolType.get_codes():
            raise ParamsError('参数不支持! (pool_type){}'.format(self.input.pool_type))

        return func(self, *args, **kwargs)
    return wrapper

