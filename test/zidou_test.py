from bases.globals import settings
from extensions.zidou import ZiDou

if __name__ == "__main__":
    phone = ''
    chatroom_id = ''

    zidou_conf = settings['THIRD_SETTING']['zidou'][phone]
    zidou = ZiDou(zidou_conf['url'], zidou_conf['secret'], phone, zidou_conf['bot_nickname'])

    # resp = zidou.set_chatroom_msg_callback('https://xj.prism-advisor.com/api/v1/chatbot/wechat_group/chatroom_msg_callback')
    # print(resp.json())

    # # OK
    # resp = zidou.get_chatroom_list()
    # print(resp.json())

    # # OK, send text message
    # resp = zidou.send_text_message([chatroom_id], 'hi again')
    # print(resp.json())

    # OK, send link message
    # resp = zidou.send_link_message(
    #     chatroom_name = [chatroom_id], 
    #     source_url='',
    #     title='',
    #     description='',
    #     image_url=''
    # )
    # print(resp.json())

    # # OK, send pic message
    # filename = ''
    # with open(filename, 'rb') as fin:
        # pic_id = zidou.upload_pic_material(
        #     fin
        # )
        # resp = zidou.send_pic_message(
        #     chatroom_name = [chatroom_id], 
        #     pic_id=pic_id
        # )
        # print(resp.json())
