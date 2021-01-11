import sys
import requests

def get_daily_message():
    get_url = 'https://www.prism-advisor.com/api/v1/chatbot/market/daily_report'
    req_headers = {
        'Content-Type': 'application/json'
    }
    msg = requests.get(get_url, headers=req_headers).json()['data']
    print(f'msg: {msg}')

    return msg

def send_daily_message(msg, chatroomname):
    post_url = 'https://xj.prism-advisor.com/api/v1/chatbot/wechat_group/send_msg'
    data = {
        "type": "text",
        "chatroomname": chatroomname,
        "content": msg
    }
    resp = requests.post(post_url, json=data)
    
    print(f'post resp: {resp}')


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('chatroomname is needed!')
        exit()

    msg = get_daily_message()

    for chatroomname in sys.argv[1:]:
        send_daily_message(msg, chatroomname)
