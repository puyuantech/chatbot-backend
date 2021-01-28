
from flask import jsonify, current_app, request

from bases.exceptions import VerifyError
from models import WechatGroupBotConfig
from utils.decorators import view_login_required
from utils.helper import RedPrint, ERROR_RSP, SUCCESS_RSP

from .logic import ChatbotLogic


api = RedPrint('')


@api.route("/api/v1/chatbot/user/list", methods=["GET"])
@view_login_required
def _get_user_list():
    """查询用户列表"""
    # TODO: 分页
    self_logic = ChatbotLogic(current_app.logger)
    top_n = request.args.get('top_n')
    wechat_group_id = request.args.get('wechat_group_id')
    if top_n:
        top_n = int(top_n)
        if top_n <= 0:
            raise VerifyError('top_n参数不合法！')
    data = self_logic.get_user_list(top_n, wechat_group_id)
    return SUCCESS_RSP(data)


@api.route("/api/v1/chatbot/user/info", methods=["GET"])
def _get_user_info():
    """查询用户信息"""
    self_logic = ChatbotLogic(current_app.logger)
    user_id = request.args.get('user_id')
    rsvp_user_id = request.args.get('rsvp_user_id')
    if not user_id and not rsvp_user_id:
        raise VerifyError('缺少用户ID！')
    data = self_logic.get_user_info(user_id=user_id, rsvp_user_id=rsvp_user_id)
    return SUCCESS_RSP(data)


@api.route("/api/v1/chatbot/user/dialog", methods=["GET"])
@view_login_required
def _get_user_dialog():
    """查询用户对话记录"""
    # TODO: 分页
    self_logic = ChatbotLogic(current_app.logger)
    user_id = request.args.get('user_id')
    if not user_id:
        raise VerifyError('缺少用户ID！')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    data = self_logic.get_user_dialog(user_id, start_time, end_time)
    return SUCCESS_RSP(data)


@api.route("/api/v1/chatbot/wechat_group/dialog", methods=["GET"])
@view_login_required
def _get_wechat_group_dialog():
    """查询用户对话记录"""
    # TODO: 分页
    self_logic = ChatbotLogic(current_app.logger)

    wechat_group_id = request.args.get('wechat_group_id')
    if not wechat_group_id:
        raise VerifyError('缺少微信群ID！')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    data = self_logic.get_wechat_group_dialog(wechat_group_id, start_time, end_time)
    return SUCCESS_RSP(data)


@api.route("/api/v1/chatbot/wechat_group/bot_config", methods=["GET"])
@view_login_required
def _get_wechat_group_bot_config():
    """查询微信群对话机器人配置"""
    self_logic = ChatbotLogic(current_app.logger)

    wechat_group_id = request.args.get('wechat_group_id')
    if not wechat_group_id:
        raise VerifyError('缺少微信群ID！')

    data = self_logic.get_wechat_group_bot_config(wechat_group_id)
    return SUCCESS_RSP(data)


@api.route("/api/v1/chatbot/wechat_group/bot_config", methods=["POST"])
@view_login_required
def _set_wechat_group_bot_config():
    """设置微信群对话机器人配置"""
    wechat_group_id = request.json.get('wechat_group_id')
    bot_id = request.json.get('bot_id')
    share_token = request.json.get('share_token')
    stage = request.json.get('stage')
    be_at = request.json.get('be_at')
    if not wechat_group_id or not bot_id or not share_token:
        raise VerifyError('缺少必要参数！')

    WechatGroupBotConfig.update_bot_config(wechat_group_id, bot_id, share_token, stage, be_at)
    return SUCCESS_RSP()


@api.route("/api/v1/chatbot/user/dialog", methods=["POST"])
def _update_user_dialog():
    """记录用户对话"""
    self_logic = ChatbotLogic(current_app.logger)

    # self.logger.info(request.json)
    self_logic.update_user_dialog(request.json)
    return SUCCESS_RSP()


@api.route("/api/v1/chatbot/user/tag", methods=["POST"])
def _update_user_tag():
    """更新用户标签"""
    self_logic = ChatbotLogic(current_app.logger)

    rsvp_user_id = request.json.get('rsvp_user_id')
    tag_type = request.json.get('tag_type')
    tag_value = request.json.get('tag_value')
    operation = request.json.get('operation')
    self_logic.update_user_tag(rsvp_user_id, tag_type, tag_value, operation)
    return SUCCESS_RSP()


@api.route("/api/v1/chatbot/user/product_view", methods=["POST"])
def _update_user_product_view():
    """记录用户产品浏览"""
    self_logic = ChatbotLogic(current_app.logger)

    rsvp_user_id = request.json.get('user_id')
    wechat_group_id = request.json.get('group')
    product_id = request.json.get('product_id')
    product_type = request.json.get('product_type')
    product_name = request.json.get('product_name')
    ts = request.json.get('ts')
    if None in (rsvp_user_id, product_id, product_type, product_name):
        raise VerifyError('缺少用户ID或产品信息！')
    data = self_logic.update_user_product_view(rsvp_user_id, wechat_group_id, product_id, product_type, product_name, ts)
    return SUCCESS_RSP(data)


@api.route("/api/v1/chatbot/bot_info", methods=["GET"])
def _bot_info():
    """获取聊天机器人信息（用于小程序前端展示）"""
    self_logic = ChatbotLogic(current_app.logger)

    resp = self_logic.get_bot_info()
    if not resp:
        return ERROR_RSP()
    return SUCCESS_RSP(resp)


@api.route("/api/v1/chatbot/chat", methods=["POST"])
def _chat():
    """聊天"""
    self_logic = ChatbotLogic(current_app.logger)

    resp = self_logic.chat(request.json)
    if not resp:
        return ERROR_RSP()
    return SUCCESS_RSP(resp)


@api.route("/api/v1/chatbot/wechat_group/chatroom_msg_callback", methods=["POST"])
def _wechat_chatroom_msg_callback():
    """微信群成员聊天记录及回复"""
    self_logic = ChatbotLogic(current_app.logger)

    self_logic.wechat_chatroom_msg_callback(
        request.json,
        current_app.chatroom_member_info_dict,
        current_app.chatroom_zidou_account_dict
    )
    return SUCCESS_RSP()


@api.route("/api/v1/chatbot/wechat_group/send_msg", methods=["POST"])
def _send_msg():
    """微信群成员聊天记录及回复"""
    self_logic = ChatbotLogic(current_app.logger)
    self_logic.send_msg(request.json, current_app.chatroom_zidou_account_dict)
    return SUCCESS_RSP()


@api.route("/api/v1/chatbot/wechat_group/list", methods=["GET"])
@view_login_required
def _get_wechat_group_list():
    """查询微信群列表"""
    self_logic = ChatbotLogic(current_app.logger)

    # TODO: 分页
    data = self_logic.get_wechat_group_list(
        current_app.chatroom_member_info_dict,
        current_app.chatroom_zidou_account_dict
    )
    return SUCCESS_RSP(data)


@api.route("/api/v1/chatbot/cognai/dialog", methods=["GET"])
def _get_cognai_dialog():
    """查询用户对话量分布统计"""
    self_logic = ChatbotLogic(current_app.logger)
    q = request.args.get('q')

    rsp = self_logic.get_cognai_dialog(q)

    return jsonify(rsp), 200

