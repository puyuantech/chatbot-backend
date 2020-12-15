
from bases.viewhandler import ApiViewHandler
from models import ChatbotDialogTag, ChatbotTag, User
from utils.decorators import login_required, params_required

from .libs.dialogs import get_dialogs_info


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

