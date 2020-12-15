
from sqlalchemy import func

from bases.globals import db
from models import ChatbotDialog, ChatbotDialogTag, User


def get_tags_info(tags):
    tags_info = []
    for tag in tags:
        query = ChatbotDialogTag.filter_by_query(tag_name=tag.tag_name)
        dialog_tag = query.order_by(ChatbotDialogTag.create_time.desc()).first()

        tags_info.append({
            **tag.to_dict(remove_fields_list=['update_time']),
            'dialog_count': query.count(),
            'nick_name': User.get_by_id(tag.user_id).nick_name,
            'latest_dialog': dialog_tag and ChatbotDialog.get_by_id(dialog_tag.dialog_id).to_dict(
                remove_fields_list=['create_time', 'update_time']
            ),
        })
    return tags_info


def get_tags_by_dialog_id(dialog_id):
    dialog_tags = ChatbotDialogTag.filter_by_query(dialog_id=dialog_id).all()
    return [{
            'tag_id': dialog_tag.id,
            'tag_name': dialog_tag.tag_name,
        } for dialog_tag in dialog_tags
    ]


def get_top_tags():
    tag_names = db.session.query(
        ChatbotDialogTag.tag_name
    ).filter_by(is_deleted=False).group_by(
        ChatbotDialogTag.tag_name
    ).order_by(
        func.count(ChatbotDialogTag.id).desc()
    ).limit(10).all()
    return [tag_name for tag_name, in tag_names]

