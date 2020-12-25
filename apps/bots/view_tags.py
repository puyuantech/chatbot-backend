from flask import g
from bases.exceptions import VerifyError
from bases.viewhandler import ApiViewHandler
from models.chat_bot import ChatbotDialogTag, ChatbotTag
from utils.decorators import login_required, params_required, permission_required

from .libs.tags import get_tags_info, get_top_tags


class TagsAPI(ApiViewHandler):

    @login_required
    @permission_required('标签中心')
    def get(self):
        tags = ChatbotTag.filter_by_query().all()
        return get_tags_info(tags)


class TopTagsAPI(ApiViewHandler):

    @login_required
    def get(self):
        return get_top_tags()


class TagAPI(ApiViewHandler):

    @login_required
    @params_required(*['dialog_id', 'tag_name'])
    def post(self):
        """添加对话标签"""
        if ChatbotDialogTag.filter_by_query(
            tag_name=self.input.tag_name,
            dialog_id=self.input.dialog_id,
        ).one_or_none():
            raise VerifyError('标签已存在!')

        if not ChatbotTag.filter_by_query(tag_name=self.input.tag_name).one_or_none():
            ChatbotTag.create(
                tag_name=self.input.tag_name,
                user_id=g.user.id,
            )

        dialog_tag = ChatbotDialogTag.create(
            tag_name=self.input.tag_name,
            dialog_id=self.input.dialog_id,
            add_user_id=g.user.id,
        )

        return {'tag_id': dialog_tag.id}

    @login_required
    @params_required(*['tag_id'])
    def delete(self):
        """删除对话标签"""
        dialog_tag = ChatbotDialogTag.get_by_id(self.input.tag_id)
        dialog_tag.update(
            is_deleted=True,
            del_user_id=g.user.id,
        )
        return 'success'

