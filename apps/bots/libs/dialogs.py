
from bases.globals import db
from models import ChatbotDialog, ChatbotDialogStat, ChatbotUserInfo, ChatbotUserStat

from .tags import get_tags_by_dialog_id


def get_dialogs_info(dialog_ids: dict):
    dialogs = db.session.query(
        ChatbotDialog
    ).filter(
        ChatbotDialog.id.in_(dialog_ids.keys())
    ).order_by(
        ChatbotDialog.ts.desc()
    ).all()

    result = []
    for dialog in dialogs:
        result.append({
            'tags': get_tags_by_dialog_id(dialog.id),
            'tag_create_time': dialog_ids[dialog.id],
            'nick_name': ChatbotUserInfo.get_by_id(dialog.user_id).nick_name,
            **dialog.to_dict(remove_fields_list=['create_time', 'update_time']),
        })
    return result


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

