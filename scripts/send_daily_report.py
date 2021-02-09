import sys
import datetime
import requests

def get_last_trading_day():
    get_url = 'https://www.prism-advisor.com/api/v1/cashbook/max_trading_date'
    req_headers = {
        'Content-Type': 'application/json'
    }
    last_trading_day_str = requests.get(get_url, headers=req_headers).json()['data']
    last_trading_day = datetime.datetime.strptime(last_trading_day_str, '%Y-%m-%d').date()

    return last_trading_day

def get_index_daily_report():
    get_url = 'https://www.prism-advisor.com/api/v1/chatbot/market/index_daily_report'
    req_headers = {
        'Content-Type': 'application/json'
    }
    msg = requests.get(get_url, headers=req_headers).json()['data']
    print(f'index_daily_report: {msg}')

    return msg

def get_sector_daily_report():
    get_url = 'https://www.prism-advisor.com/api/v1/chatbot/market/sector_daily_report'
    req_headers = {
        'Content-Type': 'application/json'
    }
    msg = requests.get(get_url, headers=req_headers).json()['data']
    print(f'sector_daily_report: {msg}')

    return msg

def get_daily_message(bot_name):
    msg = ''

    index_daily_report = get_index_daily_report()
    sector_daily_report = get_sector_daily_report()

    for market_indexes in index_daily_report:
        market_type = market_indexes['market_type']
        msg += f'【{market_type}】\n'

        indexes = market_indexes['indexes']
        for index in indexes:
            index_name = index['index_name']
            close = index['close']
            daily_ret = index['daily_ret']
            daily_ret_prefix = '' if daily_ret < 0 else '+'
            msg += f'{index_name}：{close} ({daily_ret_prefix}{daily_ret}%)\n'

        if market_type == '国内市场':
            if sector_daily_report:
                sector_name_list = []
                daily_ret_list = []
                for item in sector_daily_report:
                    sector_name = item['sector_name']
                    daily_ret = item['daily_ret']
                    sector_name_list.append(sector_name)
                    daily_ret_list.append(f'{daily_ret}%')
                middle_part = '分别' if len(sector_name_list) > 1 else ''
                msg += f'{"、".join(sector_name_list)}领涨，涨幅{middle_part}为：{"、".join(daily_ret_list)}\n'

    msg += '—————————————\n'
    msg += f'您可以 @{bot_name} 并提问：\n'
    msg += '易方达瑞恒怎么样？\n'
    msg += '易方达中小盘和易方达瑞恒哪个好？\n'
    msg += '张坤怎么样？\n'
    msg += '新能源基金有哪些？\n'

    return msg

def send_daily_message(msg, chatroomname):
    post_url = 'https://xj.prism-advisor.com/api/v1/chatbot/wechat_group/send_text_msg'
    data = {
        "chatroomname": chatroomname,
        "content": msg
    }
    resp = requests.post(post_url, json=data)
    
    print(f'post resp: {resp}')

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print('Bot_name and chatroomname (list) are needed!')
        exit()

    last_trading_day = get_last_trading_day()
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    if yesterday != last_trading_day:
        print(f'Yesterday {yesterday} is not trading day! Last trading day is {last_trading_day}')
        exit()

    msg = get_daily_message(sys.argv[1])

    for chatroomname in sys.argv[2:]:
        send_daily_message(msg, chatroomname)
