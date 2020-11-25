

class EnumBase(object):

    _code_2_name_cache = None
    _name_2_code_cache = None

    @classmethod
    def _init_cache(cls):
        if cls._code_2_name_cache is None:
            cls._code_2_name_cache = {
                getattr(cls, name): name for name in dir(cls) if not name.startswith('_') and isinstance(getattr(cls, name), (int, str, bytes, float))
            }
        if cls._name_2_code_cache is None:
            cls._name_2_code_cache = {
                name: getattr(cls, name) for name in dir(cls) if not name.startswith('_') and isinstance(getattr(cls, name), (int, str, bytes, float))
            }

    @classmethod
    def read(cls, code):
        cls._init_cache()
        return cls._code_2_name_cache.get(code, code)

    @classmethod
    def parse(cls, name):
        cls._init_cache()
        return cls._name_2_code_cache.get(name)

    @classmethod
    def has_code(cls, code):
        cls._init_cache()
        return code in cls._code_2_name_cache

    @classmethod
    def has_name(cls, name):
        cls._init_cache()
        return name in cls._name_2_code_cache

    @classmethod
    def get_names(cls):
        cls._init_cache()
        return cls._name_2_code_cache.keys()

    @classmethod
    def get_codes(cls):
        cls._init_cache()
        return cls._code_2_name_cache.keys()

    @classmethod
    def get_name_2_code(cls):
        cls._init_cache()
        return cls._name_2_code_cache

    @classmethod
    def get_code_2_name(cls):
        cls._init_cache()
        return cls._code_2_name_cache

