
from bases.globals import db
from models import ChatbotDialog

from .tags import get_tags_by_dialog_id


def get_dialogs_info(dialog_ids):
    dialogs = db.session.query(
        ChatbotDialog
    ).filter(
        ChatbotDialog.id.in_(dialog_ids)
    ).order_by(
        ChatbotDialog.ts.desc()
    ).all()

    result = []
    for dialog in dialogs:
        result.append({
            'tags': get_tags_by_dialog_id(dialog.id),
            **dialog.to_dict(remove_fields_list=['create_time', 'update_time']),
        })
    return result

