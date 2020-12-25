from apps.accounts import blu as accounts_blu
from apps.admin import blu as admin_blu
from apps.auth import blu as auth_blu
from apps.bots import blu as bot_blu
from apps.captchas import blu as captcha_blu
from apps.evaluations import blu as eval_blu
from apps.fund import blu as fund_blu

routers = [
    accounts_blu,
    admin_blu,
    auth_blu,
    bot_blu,
    captcha_blu,
    eval_blu,
    fund_blu,
]

