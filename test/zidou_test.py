from bases.globals import settings
from extensions.zidou import ZiDou

if __name__ == "__main__":
    phone = ''
    zidou_conf = settings['THIRD_SETTING']['zidou'][phone]
    zidou = ZiDou(zidou_conf['url'], zidou_conf['secret'], phone, zidou_conf['bot_nickname'])

    # resp = zidou.set_chatroom_msg_callback('https://xj.prism-advisor.com/api/v1/chatbot/wechat_group/chatroom_msg_callback')
    # print(resp.json())

    resp = zidou.get_chatroom_list()
    print(resp)
