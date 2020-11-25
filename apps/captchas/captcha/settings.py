import os
from .utils import dict_to_object
from pkg_resources import resource_filename

FONT_PATH = resource_filename('apps.captchas.captcha.fonts', 'Vera.ttf')

DEFAULTS = dict_to_object({
    'CAPTCHA_CACHE': 'default',
    'CAPTCHA_TIMEOUT': 300,  # 5 minuts
    'CAPTCHA_CACHE_KEY': 'rest_captcha_{key}.{version}',
    'CAPTCHA_KEY': 'verification_key',
    'CAPTCHA_IMAGE': 'verification_image',
    'CAPTCHA_LENGTH': 4,
    'CAPTCHA_FONT_PATH': FONT_PATH,
    'CAPTCHA_FONT_SIZE': 22,
    'CAPTCHA_IMAGE_SIZE': (90, 40),
    'CAPTCHA_LETTER_ROTATION': (-35, 35),
    'CAPTCHA_FOREGROUND_COLOR': '#001100',
    'CAPTCHA_BACKGROUND_COLOR': '#ffffff',
    'FILTER_FUNCTION': 'captcha.captcha.filter_default',
    'NOISE_FUNCTION': 'captcha.captcha.noise_default',
    # for tests access: MASTER_CAPTCHA: {'secret_key: secret_value'}
    'MASTER_CAPTCHA': {},
})

