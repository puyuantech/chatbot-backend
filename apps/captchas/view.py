import uuid
import base64

from bases.viewhandler import ApiViewHandler
from utils.decorators import params_required
from models import CaptchaCode
from .captcha import captcha
from .captcha import utils
from .captcha.settings import DEFAULTS
from .libs import check_img_captcha


class GetCaptcha(ApiViewHandler):
    def get(self):
        key = str(uuid.uuid4())
        code = utils.random_char_challenge(DEFAULTS.CAPTCHA_LENGTH)

        # generate image
        image_bytes = captcha.generate_image(code)
        image_b64 = base64.b64encode(image_bytes)
        print(key, code)
        data = {
            DEFAULTS.CAPTCHA_KEY: key,
            DEFAULTS.CAPTCHA_IMAGE: image_b64.decode(),
            'image_type': 'image/png',
            'image_decode': 'base64'
        }
        CaptchaCode.create(
            key=key,
            value=code,
            expires_at=CaptchaCode.generate_expires_at()
        )
        return data


class CaptchaCheckAPI(ApiViewHandler):
    @params_required(*['verification_code', 'verification_key'])
    def post(self):
        check_img_captcha(
            verification_code=self.input.verification_code,
            verification_key=self.input.verification_key,
        )

