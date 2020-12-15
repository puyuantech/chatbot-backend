
from bases.viewhandler import ApiViewHandler
from models.chat_bot import ChatbotDialogTag
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
        dialog_tags = ChatbotDialogTag.filter_by_query(tag_name=self.input.tag_name).all()
        dialog_ids = [dialog_tag.dialog_id for dialog_tag in dialog_tags]
        return get_dialogs_info(dialog_ids)

