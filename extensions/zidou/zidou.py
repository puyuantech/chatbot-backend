
import json
import time
import random
import hashlib
import requests


class ZiDou(object):

    def __init__(self, url, secret, phone):
        self.url = url
        self.secret = secret
        self.phone = phone

    def get_nonce(self):
        '''
        生成一个随机1到8位长度的随机字符串
        '''
        base_str = list('ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789')
        length = random.randint(1, 8)
        samples = random.sample(base_str, length)
        return ''.join(samples)

    def get_sign(self, data):
        '''
        计算sign
        '''
        temp_json = dict()
        temp_json.update(data)
        pre_list = [str(k) + '=' + str(v) for k, v in temp_json.items()] 
        pre_list.sort()
        pre_str = '&'.join(pre_list) 
        pre_str = pre_str + self.secret
        m = hashlib.md5() 
        m.update(pre_str.encode()) 
        return m.hexdigest()

    def get_request_params(self, function, action, params):
        data = {
            'phone': self.phone,
            'timestamp': time.strftime('%Y%m%d%H%M%S', time.localtime(int(time.time()))),
            'nonce': self.get_nonce(),
            'function': function,
            'action': action,
            'params': json.dumps(params)
        }
        sign = self.get_sign(data) 
        data.update({'sign': sign}) 
        return data

    def get_chat_log(self, chatroom_name, start_ts, end_ts, page_id=1):
        '''
        查询群聊记录
        '''
        func = 'chatroom'
        action = 'get'
        pagesize = 50
        params = {
            'chat_record': 1,
            'chatroomname': chatroom_name,
            'start_dt': int(start_ts),
            'end_dt': int(end_ts),
            'page': page_id,
            'pagesize': pagesize
        }
        req_data = self.get_request_params(func, action, params)
        resp = requests.post(self.url, req_data).json()

        records = []
        if not resp or resp.get('err_code', 1) != 0 or not resp.get('content') or not resp['content'].get('records'):
            return records

        records = resp['content']['records']
        if page_id >= resp.get('total_page', 0):
            return records

        more_records = self.get_chat_log(chatroom_name, start_ts, end_ts, page_id + 1)
        records.extend(more_records)
        
        return records

    def get_member_info(self, chatroom_name):
        '''
        查询群成员信息
        '''
        func = 'contact'
        action = 'get'
        params = {
            'chatroomname': chatroom_name,
            'invite': 0,
        }
        req_data = self.get_request_params(func, action, params)
        resp = requests.post(self.url, req_data).json()

        member_info_dict = {}
        # print(resp.get('content'))
        if not resp or resp.get('err_code', 1) != 0 or not resp.get('content') or not resp['content'].get('members_info_dict'):
            return member_info_dict

        raw_member_info_dict = resp['content']['members_info_dict']
        for key, value in raw_member_info_dict.items():
            nickname = value.get('nickname')
            if not nickname:
                nickname = value.get('quan_pin', '')
                
            avatar_url = value.get('avatar_url', '')

            member_info_dict[key] = {
                'nickname': nickname,
                'avatar_url': avatar_url
            }

        return member_info_dict

    def get_chatroom_list(self, page_id=1):
        '''
        查询群列表
        '''
        func = 'chatroom'
        action = 'get'
        pagesize = 50
        params = {
            'page': page_id,
            'pagesize': pagesize
        }
        req_data = self.get_request_params(func, action, params)
        resp = requests.post(self.url, req_data).json()

        chatroom_list = []
        if not resp or resp.get('err_code', 1) != 0 or not resp.get('content') or not resp['content'].get('chatroom_list'):
            return chatroom_list

        chatroom_list = resp['content']['chatroom_list']
        if page_id >= resp.get('total_page', 0):
            return chatroom_list

        more_chatrooms = self.get_chatroom_list(page_id + 1)
        chatroom_list.extend(more_chatrooms)
        
        return chatroom_list

    def send_text_message(self, chatroom_name, content):
        '''
        发送文本消息
        '''
        func = 'send_msg'
        action = 'set'
        params = {
            'msg': [
                {
                    'type': 'txt',
                    'content': content
                }
            ],
            'chatroom_list': [chatroom_name]
        }
        req_data = self.get_request_params(func, action, params)

        resp = requests.post(self.url, req_data)
        return resp

    def send_link_message(self, chatroom_name, title, source_url):
        '''
        发送链接消息
        '''
        func = 'send_msg'
        action = 'set'
        params = {
            'msg': [
                {
                    'title': title,
                    'source_url': source_url
                }
            ],
            'chatroom_list': [chatroom_name]
        }
        req_data = self.get_request_params(func, action, params)

        resp = requests.post(self.url, req_data)
        return resp

    def at_somebody(self, chatroom_name, username, msg_front, msg_after):
        '''
        发送@特定人的消息
        '''
        func = 'at_somebody'
        action = 'set'
        params = {
            'chatroomname': chatroom_name,
            'username': username,
            'msg_front': msg_front,
            'msg_after': msg_after
        }
        req_data = self.get_request_params(func, action, params)

        resp = requests.post(self.url, req_data)
        return resp

    def set_chatroom_msg_callback(self, url):
        '''
        设置回调地址
        '''
        func = 'chatroom_msg_callback'
        action = 'set'
        params = {
            'callback': url
        }
        req_data = self.get_request_params(func, action, params)

        resp = requests.post(self.url, req_data)
        return resp
