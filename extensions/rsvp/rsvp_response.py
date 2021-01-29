
from extensions.url_manager import UrlManager


class RsvpResponse:

    # TODO: get similarity from stages

    def __init__(self, stages, wechat_group_id=None, be_at=0):
        self.stages = stages
        self.wechat_group_id = wechat_group_id
        self.be_at = be_at

        self.similarity = None
        self.reply = ''
        self.start_miniprogram = False

    ########
    # Util #
    ########

    def parse_mini(self, data):
        if data == '您已经在小程序中...':
            if self.wechat_group_id:
                self.start_miniprogram = True
            else:
                data = '当前环境不支持小程序，或您已经在小程序中。'
        else:
            self.reply += data + '\n'

    def parse_url(self, url: str):
        if url.startswith('https://www.prism-advisor.com/'):
            if self.wechat_group_id:
                url = f'{url}&group={self.wechat_group_id}'
            url = UrlManager.generate_short_url(url)
        return url

    def parse_clicks_and_replies(self, clicks, replies):
        if clicks:
            self.reply += '\n点击查看：\n'
            for click in clicks:
                self.reply += click

        if replies:
            head = '\n您{}可以{}说：\n'.format(
                '还' if clicks else '',
                '@我之后' if self.be_at else '',
            )
            self.reply += head

            for reply in replies:
                self.reply += reply

    def parse_item(self, item):
        if 'title' in item:
            self.reply += '\n' + item.get('title') + '\n'

        clicks, replies = [], []
        for button in item.get('buttons', []):
            if 'postback' in button:
                url = button['postback']

                if url.startswith('https://www.prism-advisor.com/'):
                    url = self.parse_url(url)
                    clicks.append(f'{url}\n')
                else:
                    replies.append(f'{url}\n')

        self.parse_clicks_and_replies(clicks, replies)

    #########
    # Parse #
    #########

    def parse_text(self, data):
        if not data:
            return

        for d in data.get('plainText', []):
            self.parse_mini(d)

    def parse_message(self, data):
        # {
        #     "message": "以下是【股票型】明星基金经理："
        # }
        if not data:
            return

        self.parse_mini(data)

    def parse_link(self, data):
        if not data:
            return

        if 'text' in data:
            self.reply +=  f'\n{data["text"]}：\n'

        if 'url' in data:
            url = self.parse_url(data['url'])
            self.reply +=  f'{url}\n'

    def parse_cards(self, data):
        if not data:
            return

        for d in data.get('cards', []):
            self.parse_item(d)

    def parse_list(self, data):
        # {
        #     "type": "horizontal",
        #     "items": [
        #         {
        #             "buttons": [
        #                 {
        #                     "postback": "易方达消费行业怎么样？",
        #                     "text": "代表作：易方达消费行业"
        #                 },
        #                 {
        #                     "postback": "https://www.prism-advisor.com/m/#/mp/fund-manager/16E872?user_id=openidgroup_wxid_sls2xwidrwea21&chatbot=true",
        #                     "text": "点击查看基金经理详情"
        #                 }
        #             ],
        #             "title": "【萧楠】消费之王，坚守价值投资，屡获奖项。现任职易方达基金，从业3015天。\n【管理基金】\n[股票型] 超过100.0%同类型基金经理，取得了年化收益20.83%的收益，最大回撤控制在27.93%。"
        #         }
        #     ]
        # }
        if not data:
            return

        for d in data.get('items', []):
            self.parse_item(d)

    def parse_quick_replies(self, data):
        # {
        #     "quickReplies": [
        #         {
        #             "postback": "好的债券型明星基金经理有哪些？",
        #             "text": "债券型明星基金经理"
        #         }
        #     ]
        # }
        if not data:
            return

        if 'quickReplies' in data:
            quick_replies = data['quickReplies']
            head = '—————————————\n您可以{}说：\n'.format(
                '@我之后' if self.be_at else '',
            )
            self.reply += head

            for quick_reply in quick_replies:
                self.reply += f'{quick_reply["postback"]}\n'

    def parse_stages(self):
        for stage in self.stages:
            self.parse_text(stage.get('text'))
            self.parse_message(stage.get('message'))
            self.parse_link(stage.get('link'))
            self.parse_cards(stage.get('cards'))
            self.parse_list(stage.get('list'))
            self.parse_quick_replies(stage.get('quickReplies'))
        return self.similarity, self.reply, self.start_miniprogram

