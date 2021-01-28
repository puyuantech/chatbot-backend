
from flask import current_app, request

from bases.exceptions import BaseError, LogicError
from bases.viewhandler import ApiViewHandler
from extensions.zidou import ZiDouBot
from utils.decorators import params_required


class TextMessageAPI(ApiViewHandler):

    @params_required(*['content'])
    def post(self):
        """发送文本消息"""
        zidou_bot = ZiDouBot.get_chatroom_zidou_bot(self.input.chatroomname, current_app.chatroom_zidou_account_dict)
        resp = zidou_bot.send_text_message(self.input.chatroomname, self.input.content)
        current_app.logger.info(resp.json())
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

        zidou_bot = ZiDouBot.get_chatroom_zidou_bot(self.input.chatroomname, current_app.chatroom_zidou_account_dict)
        resp = zidou_bot.send_link_message(
            chatroom_name=self.input.chatroomname,
            source_url=source_url,
            title=title,
            description=description,
            image_url=image_url,
        )
        current_app.logger.info(resp.json())
        return 'success'


class PicMessageAPI(ApiViewHandler):

    def post(self):
        """发送图片消息"""
        file_obj = request.files.get('file')
        if not file_obj:
            raise LogicError('需要 files!')

        zidou_bot = ZiDouBot.get_chatroom_zidou_bot(self.input.chatroomname, current_app.chatroom_zidou_account_dict)
        pic_id = zidou_bot.upload_pic_material(file_obj)
        if not pic_id:
            raise BaseError('Failed to upload pic material!')

        resp = zidou_bot.send_pic_message(self.input.chatroomname, pic_id)
        current_app.logger.info(resp.json())
        return 'success'

