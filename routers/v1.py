from apps.accounts import blu as accounts_blu
from apps.auth import blu as auth_blu
from apps.captchas import blu as captcha_blu
from apps.admin import blu as admin_blu
from apps.bots import blu as bot_blu
from apps.evaluations import blu as eval_blu

routers = [
    auth_blu,
    accounts_blu,
    captcha_blu,
    admin_blu,
    bot_blu,
    eval_blu,
]

