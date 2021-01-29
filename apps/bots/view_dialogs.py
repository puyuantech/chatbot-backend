
import json

from collections import defaultdict
from datetime import datetime

from bases.viewhandler import ApiViewHandler
from extensions.rsvp import RsvpResponse
from models import ChatbotDialog, ChatbotDialogTag, ChatbotTag, ChatbotUserInfo, User
from utils.decorators import login_required, params_required

from .libs.dialogs import get_dialogs_info, save_chatbot_dialog
from .libs.tags import get_tags_by_dialog_id
from .libs.users import get_user_id_from_rsvp


class DialogsByTagAPI(ApiViewHandler):

    @login_required
    @params_required(*['tag_name'])
    def get(self):
        """
        1. 按添加标签的时间分页
        2. 按对话日志的时间分页
        """
        tag = ChatbotTag.get_by_query(tag_name=self.input.tag_name)
        dialog_tags = ChatbotDialogTag.filter_by_query(tag_name=self.input.tag_name).all()
        dialog_ids = {dialog_tag.dialog_id: dialog_tag.create_time.strftime('%Y-%m-%d %H:%M:%S') for dialog_tag in dialog_tags}
        return {
            **tag.to_dict(remove_fields_list=['update_time']),
            'nick_name': User.get_by_id(tag.user_id).nick_name,
            'dialogs': get_dialogs_info(dialog_ids)
        }


class DialogsByUserAPI(ApiViewHandler):

    @login_required
    @params_required(*['user_id'])
    def get(self):
        """查询用户对话记录(TODO: 分页)"""
        dialogs = ChatbotDialog.get_user_dialogs(self.input.user_id, self.input.start_time, self.input.end_time)
        return [
            {
                'tags': get_tags_by_dialog_id(dialog.id),
                **dialog.to_dict(remove_fields_list=['create_time', 'update_time']),
            }
            for dialog in dialogs
        ]

    def post(self):
        """记录用户对话"""
        req, res = self.input.request, self.input.response
        if not req or not res:
            return

        ts = datetime.fromtimestamp(req['timestamp']) if req.get('timestamp') else datetime.now()

        user_id = get_user_id_from_rsvp(req.get('uid'), ts)
        if not user_id:
            return

        similarity, bot_reply, _ = RsvpResponse(res.get('stage', [])).parse_stages()
        user_input = req.get('question')
        bot_raw_reply = json.dumps(res, ensure_ascii=False)
        save_chatbot_dialog(user_id, user_input, bot_reply, bot_raw_reply, similarity, ts)

        return 'success'


class DialogsByWechatAPI(ApiViewHandler):

    @login_required
    @params_required(*['wechat_group_id'])
    def get(self):
        """查询群用户对话记录(TODO: 分页)"""
        user_info = defaultdict(dict)
        user_info.update({
            user.id: {'nick_name': user.nick_name, 'head_img': user.head_img}
            for user in ChatbotUserInfo.filter_by_query().all()
        })

        dialogs = ChatbotDialog.get_group_dialogs(self.input.wechat_group_id, self.input.start_time, self.input.end_time)
        return [
            {
                'tags': get_tags_by_dialog_id(dialog.id),
                'nickname': user_info[dialog.user_id].get('nick_name'),
                'head_img': user_info[dialog.user_id].get('head_img'),
                **dialog.to_dict(remove_fields_list=['create_time', 'update_time']),
            }
            for dialog in dialogs
        ]

