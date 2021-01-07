from extensions.url_manager import UrlManager

if __name__ == "__main__":
    url = UrlManager.generate_short_url('https://xj.prism-advisor.com/api/v1/chatbot/wechat_group/chatroom_msg_callback')
    print(url)
