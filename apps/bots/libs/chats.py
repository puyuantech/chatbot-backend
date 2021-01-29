
from bases.globals import db
from models import WechatGroupBotConfig


def get_wechat_group_bot_config(self, wechat_group_id):
    bot_config = db.session.query(WechatGroupBotConfig).filter_by(wechat_group_id=wechat_group_id).one_or_none()

    result = {'wechat_group_id': wechat_group_id}
    if not bot_config:
        rsvp_group_conf = self.conf['rsvp_group']
        result['bot_id'] = rsvp_group_conf['bot_id']
        result['share_token'] = rsvp_group_conf['share_token']
        result['stage'] = 'release'
        result['be_at'] = 0
    else:
        result['bot_id'] = bot_config.bot_id
        result['share_token'] = bot_config.share_token
        result['stage'] = bot_config.stage
        result['be_at'] = bot_config.be_at

    return result

