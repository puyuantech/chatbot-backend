
from models import (ChatbotDialog, ChatbotDialogStat, ChatbotProductDailyView,
                    ChatbotProductView, ChatbotUserInfo, ChatbotUserStat)


def get_user_dict(user: ChatbotUserInfo, user_dialog_count=None):
    if user_dialog_count is None:
        dialog_count = ChatbotDialogStat.get_user_dialog_count(user.id)
    else:
        dialog_count = user_dialog_count.get(user.id, 0)

    user_dict = user.to_dict(remove_fields_list=['update_time'])
    user_dict['source'] = '微信群' if user_dict.pop('wechat_user_name') else '小程序'
    user_dict['user_id'] = user_dict.pop('id')
    user_dict['dialog_count'] = dialog_count
    return user_dict


def get_user_id_from_rsvp(rsvp_user_id, ts):
    if len(rsvp_user_id) <= 12:
        return

    source = rsvp_user_id[6:12]
    if source == 'prism_':
        return ChatbotUserInfo.user_active_by_id(rsvp_user_id[12:], ts)
    elif source == 'group_':
        return ChatbotUserInfo.user_active_by_wechat(rsvp_user_id[12:], ts)


def save_chatbot_dialog(user_id, user_input, bot_reply, bot_raw_reply, similarity, ts, wechat_group_id=None):
    ChatbotDialog(
        user_id=user_id,
        user_input=user_input,
        bot_reply=bot_reply,
        bot_raw_reply=bot_raw_reply,
        similarity=similarity,
        ts=ts,
        wechat_group_id=wechat_group_id,
    ).save()
    ChatbotDialogStat.update_dialog_stat(user_id, ts.date(), wechat_group_id)
    ChatbotUserStat.update_user_stat(ts.date())


def save_product_view(user_id, product_id, product_type, product_name, ts, wechat_group_id=None):
    ChatbotProductView(
        user_id=user_id,
        product_id=product_id,
        product_type=product_type,
        product_name=product_name,
        ts=ts,
        wechat_group_id=wechat_group_id,
    ).save()
    ChatbotProductDailyView.update_product_daily_view(user_id, ts.date(), wechat_group_id)

