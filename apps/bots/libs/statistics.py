
from datetime import datetime, timedelta

from models import ChatbotDialogStat, ChatbotProductDailyView, ChatbotUserStat


def get_limit_ts(ts_list, start, end):
    min_ts = min(ts_list, default=None)
    max_ts = max(ts_list, default=None)

    if start:
        start = datetime.fromisoformat(start)
        min_ts = min(min_ts, start) if min_ts else start

    if end:
        end = datetime.fromisoformat(end)
        max_ts = max(max_ts, end) if max_ts else end

    return min_ts, max_ts, start, end


def get_user_count(start, end):
    ts_count_dict = ChatbotUserStat.get_ts_counts(start, end)
    min_ts, max_ts, start, end = get_limit_ts(ts_count_dict.keys(), start, end)

    ts_list, user_count_list, new_user_count_list, active_user_count_list = [], [], [], []
    cur_ts, last_user_count = min_ts, 0
    if min_ts and max_ts:
        while cur_ts <= max_ts:
            user_count = max(ts_count_dict.get(cur_ts, {}).get('user_count', 0), last_user_count)
            active_user_count = ts_count_dict.get(cur_ts, {}).get('active_user_count', 0)

            ts_list.append(cur_ts)
            user_count_list.append(user_count)
            new_user_count_list.append(user_count - last_user_count)
            active_user_count_list.append(active_user_count)

            last_user_count = user_count
            cur_ts += timedelta(days=1)

    return {
        'ts': ts_list,
        'user_count': user_count_list,
        'new_user_count': new_user_count_list,
        'active_user_count': active_user_count_list
    }


def get_ts_counts(count_dict, min_ts, max_ts):
    ts_list, count_list, cur_ts = [], [], min_ts
    if min_ts and max_ts:
        while cur_ts <= max_ts:
            ts_list.append(cur_ts)
            count_list.append(count_dict.get(cur_ts, 0))
            cur_ts += timedelta(days=1)
    return {'ts_list': ts_list, 'count_list': count_list}


def get_dialog_count(user_id=None, start=None, end=None):
    dialog_count_dict = ChatbotDialogStat.get_ts_dialog_counts(user_id, start, end)
    min_ts, max_ts, start, end = get_limit_ts(dialog_count_dict.keys(), start, end)

    ts_counts = get_ts_counts(dialog_count_dict, min_ts, max_ts)
    return {'ts': ts_counts['ts_list'], 'dialog_count': ts_counts['count_list']}


def get_product_daily_view(user_id=None, start=None, end=None):
    product_view_count_dict = ChatbotProductDailyView.get_ts_product_view_counts(user_id, start, end)
    min_ts, max_ts, start, end = get_limit_ts(product_view_count_dict.keys(), start, end)

    ts_counts = get_ts_counts(product_view_count_dict, min_ts, max_ts)
    return {'ts': ts_counts['ts_list'], 'product_view_count': ts_counts['count_list']}

