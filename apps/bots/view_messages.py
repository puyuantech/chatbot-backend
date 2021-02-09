
from flask import current_app, request

from bases.exceptions import BaseError, LogicError
from bases.viewhandler import ApiViewHandler
from extensions.zidou import ZiDouBot
from utils.decorators import params_required
from .libs.messages import save_text_message, save_link_message, save_pic_message, get_messages

class TextMessageAPI(ApiViewHandler):

    @params_required(*['content'])
    def post(self):
        """发送文本消息"""
        chatroom_list = self.input.chatroomname.split(',')
        for chatroomname in chatroom_list:
            zidou_bot = ZiDouBot.get_chatroom_zidou_bot(chatroomname, current_app.chatroom_zidou_account_dict)
            resp = zidou_bot.send_text_message(chatroomname, self.input.content)
            current_app.logger.info(f'[send_text_message] (response){resp.json()}')
            save_text_message(user_id=1, chatroomname=chatroomname, text=self.input.content)
        return 'success'


class LinkMessageAPI(ApiViewHandler):

    @params_required(*['content'])
    def post(self):
        """发送链接消息"""
        content = self.input.content
        source_url = content.get('source_url')
        title = content.get('title', '')
        description = content.get('description', '')
        image_url = content.get('image_url', '')
        if not source_url:
            raise LogicError('需要 source_url 参数')

        chatroom_list = self.input.chatroomname.split(',')
        for chatroomname in chatroom_list:
            zidou_bot = ZiDouBot.get_chatroom_zidou_bot(chatroomname, current_app.chatroom_zidou_account_dict)
            resp = zidou_bot.send_link_message(
                chatroom_name=chatroomname,
                source_url=source_url,
                title=title,
                description=description,
                image_url=image_url,
            )
            current_app.logger.info(f'[send_link_message] (response){resp.json()}')
            save_link_message(user_id=1, chatroomname=chatroomname, link_source_url=source_url, link_title=title,
                              link_description=description, link_image_url=image_url)
        return 'success'


class PicMessageAPI(ApiViewHandler):

    def post(self):
        """发送图片消息"""
        file_obj = request.files.get('file')
        if not file_obj:
            raise LogicError('需要 files!')

        chatroom_list = self.input.chatroomname.split(',')
        zidou_bot_pic_material = {}
        for chatroomname in chatroom_list:
            zidou_bot = ZiDouBot.get_chatroom_zidou_bot(chatroomname, current_app.chatroom_zidou_account_dict)

            if zidou_bot.phone not in zidou_bot_pic_material:
                pic_id = zidou_bot.upload_pic_material(file_obj)
                if not pic_id:
                    raise BaseError('Failed to upload pic material!')
                file_obj.seek(0)
                zidou_bot_pic_material[zidou_bot.phone] = pic_id

            pic_id = zidou_bot_pic_material[zidou_bot.phone]

            resp = zidou_bot.send_pic_message(chatroomname, pic_id)
            current_app.logger.info(f'[send_pic_message] (response){resp.json()}')
            # # Upload and save pic message
            # save_pic_message(user_id=1, chatroomname=chatroomname, 
            #                  pic_url='https://goss1.cfp.cn/creative/vcg/800/version23/VCG41175510742.jpg')
        return 'success'


class MessageHistoryAPI(ApiViewHandler):

    def get(self):
        """获取消息发送记录"""
        chatroomnames = self.input.chatroomname if self.input.chatroomname else []
        page_index = int(self.input.page_index) if self.input.page_index else 0
        page_size = int(self.input.page_size) if self.input.page_size else 20
        return get_messages(chatroomnames=chatroomnames, page_index=page_index, page_size=page_size, 
                            start_time=self.input.start_time, end_time=self.input.end_time)
