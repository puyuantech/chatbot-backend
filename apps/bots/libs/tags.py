
from sqlalchemy import func

from bases.globals import db
from models.chat_bot import ChatbotDialogTag


def get_top_tags():
    tag_names = db.session.query(
        ChatbotDialogTag.tag_name
    ).filter_by(is_deleted=False).group_by(
        ChatbotDialogTag.tag_name
    ).order_by(
        func.count(ChatbotDialogTag.id).desc()
    ).limit(10).all()
    return [tag_name for tag_name, in tag_names]


def get_tags_by_dialog_id(dialog_id):
    dialog_tags = ChatbotDialogTag.filter_by_query(dialog_id=dialog_id).all()
    return [{
            'tag_id': dialog_tag.id,
            'tag_name': dialog_tag.tag_name,
        } for dialog_tag in dialog_tags
    ]

