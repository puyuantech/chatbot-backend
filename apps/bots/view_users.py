
from datetime import datetime

from bases.exceptions import VerifyError
from bases.globals import db
from bases.viewhandler import ApiViewHandler
from models import ChatbotDialogStat, ChatbotUserInfo
from utils.decorators import login_required, params_required

from .constants import EMPTY_VALUE, Operation, TagType
from .libs.users import get_user_dict, get_user_id_from_rsvp, save_product_view


class UserInfoAPI(ApiViewHandler):

    def get(self):
        """查询用户信息"""
        user_id, rsvp_user_id = self.input.user_id, self.input.rsvp_user_id
        if not user_id and not rsvp_user_id:
            raise VerifyError('缺少用户ID！')

        if not user_id:
            user_id = get_user_id_from_rsvp(rsvp_user_id, datetime.now())
            if not user_id:
                return {}

        user = db.session.query(ChatbotUserInfo).filter_by(id=user_id).one_or_none()
        return get_user_dict(user)


class UserListAPI(ApiViewHandler):

    @login_required
    def get(self):
        """查询用户列表"""
        top_n = self.input.top_n
        if top_n:
            top_n = int(top_n)
            if top_n <= 0:
                raise VerifyError('top_n参数不合法！')

        user_dialog_count = ChatbotDialogStat.get_user_dialog_counts(top_n)

        query = ChatbotUserInfo.filter_by_query()
        if top_n:
            query = query.filter(ChatbotUserInfo.id.in_(user_dialog_count.keys()))
        users = query.all()

        result = [get_user_dict(user, user_dialog_count) for user in users]
        if top_n:
            result.sort(key=lambda item: item.get('dialog_count', -1), reverse=True)

        return result


class UserTagAPI(ApiViewHandler):

    @params_required(*['rsvp_user_id', 'tag_type', 'tag_value', 'operation'])
    def post(self):
        """更新用户标签"""
        user_id = get_user_id_from_rsvp(self.input.rsvp_user_id, datetime.now())
        if not user_id:
            return

        chatbot_user = db.session.query(ChatbotUserInfo).filter_by(id=user_id).one_or_none()
        if not chatbot_user:
            return

        tag_value = None if self.input.tag_value in EMPTY_VALUE else float(self.input.tag_value)

        if self.input.tag_type == TagType.expertise:
            if self.input.operation == Operation.set:
                chatbot_user.expertise = tag_value
            if self.input.operation == Operation.update:
                chatbot_user.expertise += tag_value

            chatbot_user.expertise = min(chatbot_user.expertise, 1)
            chatbot_user.expertise = max(chatbot_user.expertise, 0)

        if self.input.tag_type == TagType.risk_tolerance:
            if self.input.operation == Operation.set:
                chatbot_user.risk_tolerance = tag_value
            elif self.input.operation == Operation.update:
                chatbot_user.risk_tolerance += tag_value

            chatbot_user.risk_tolerance = min(chatbot_user.risk_tolerance, 1)
            chatbot_user.risk_tolerance = max(chatbot_user.risk_tolerance, 0)

        db.session.commit()
        return 'success'


class UserProductViewAPI(ApiViewHandler):

    @params_required(*['user_id', 'product_id', 'product_type', 'product_name'])
    def post(self):
        """记录用户产品浏览"""
        rsvp_user_id, ts = self.input.user_id, self.input.ts
        ts = ts if ts else datetime.now()
        if type(ts) is str:
            ts = datetime.fromisoformat(ts)

        user_id = get_user_id_from_rsvp(rsvp_user_id, ts)
        if not user_id:
            return

        save_product_view(
            user_id, self.input.product_id, self.input.product_type,
            self.input.product_name, ts, self.input.group
        )
        return 'success'

