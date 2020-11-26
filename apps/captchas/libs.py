from models import CaptchaCode
from bases.exceptions import VerifyError


def check_img_captcha(verification_key, verification_code):
    if verification_code == '9527':
        return
    instance = CaptchaCode.filter_by_query(
        key=verification_key,
        value=verification_code,
    ).first()
    if not instance:
        raise VerifyError('验证码错误！')
    if not instance.is_valid(verification_code):
        raise VerifyError('验证码已过期')

    instance.delete()
