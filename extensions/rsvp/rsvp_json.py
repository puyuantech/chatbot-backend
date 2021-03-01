
import json

from extensions.url_manager import UrlManager

from .rsvp_response import RsvpResponse


class RsvpJson:

    # TODO: get similarity from stages

    def __init__(self, response, wechat_group_id=None, be_at=0, short_url=True):
        self.stages = response.get('stage', [])
        self.data = None
        for stage in self.stages:
            try:
                self.data = json.loads(stage['message'])['text']
            except Exception:
                break

        self.wechat_group_id = wechat_group_id
        self.be_at = be_at
        self.short_url = short_url

        self.similarity = None
        self.reply = ''
        self.start_miniprogram = False

    def parse_url(self, url: str):
        if self.short_url and url.startswith('https://www.prism-advisor.com/'):
            if self.wechat_group_id:
                url = f'{url}&group={self.wechat_group_id}'
            url = UrlManager.generate_short_url(url)
        return url

    def parse_position(self, position, name_key_type, weight_key_type=None, range_num=10):
        for i in range(1, range_num + 1):
            name_key, weight_key = f'rank{i}_{name_key_type}', f'rank{i}_{weight_key_type or name_key_type}weight'
            if name_key not in position:
                return
            self.reply += f"{position[name_key]}：{position[weight_key]}%\n"

    ########
    # Util #
    ########

    def parse_message(self, message_detail, data):
        if message_detail == 'mini':
            assert data == '您已经在小程序中...'
            if self.wechat_group_id:
                self.start_miniprogram = True
            else:
                data = '当前环境不支持小程序，或您已经在小程序中。'
            self.reply += data

        elif message_detail == 'link':
            self.reply += data['key'] + '\n' + self.parse_url(data['value'])

        elif message_detail == 'text':
            self.reply += data

        elif message_detail == 'error':
            # TODO: save error log
            self.reply += data

    def parse_fund(self, data):
        for d in data:
            message = f"{d['基金名称']}，{d['基金类型']}，棱镜评分超过{d.get('基金评分', '--')}%的同类型基金。" +\
                      f"由{d['基金公司']}管理，基金经理{d['基金经理']}，棱镜评分超过{d.get('基金经理评分', '--')}%的同类型基金经理。" +\
                      f"{d['成立日期']}成立，到目前为止取得了年化收益率{d['成立至今年化收益率']}%的成绩，最大回撤控制在{d['最大回撤']}%，" +\
                      f"目前的基金规模为{d['基金规模']}亿。投资风格为{d.get('基金投资风格规模', '--')}{d.get('基金投资风格类型', '--')}。\n" +\
                      f"点击查看详情：{self.parse_url(d['基金详情链接'])}"
            self.reply += '\n' + message + '\n'

    def parse_fund_position(self, data):
        if data.get('十大重仓股') and data['十大重仓股'].get('rank1_stock'):
            self.reply += f"【十大重仓股】\n"
            self.parse_position(data['十大重仓股'], 'stock')

        if data.get('十大重仓债') and data['十大重仓债'].get('rank1_bond'):
            self.reply += f"【十大重仓债】\n"
            self.parse_position(data['十大重仓债'], 'bond')

        if data.get('行业配置') and data['行业配置'].get('rank1_indname'):
            self.reply += f"【前三大行业占比】\n"
            self.parse_position(data['行业配置'], 'indname', 'ind', 3)

    def parse_fund_market(self, data):
        message = f"以下是{data['基金名称']}的近期收益率：\n" +\
                  f"近1周收益率：{data['近一周收益率']}%\n" +\
                  f"近1月收益率：{data['近一月收益率']}%\n" +\
                  f"近3月收益率：{data['近一季收益率']}%\n" +\
                  f"近6月收益率：{data['近半年收益率']}%\n" +\
                  f"今年以来收益率：{data['今年以来收益率']}%"
        self.reply += message

    def parse_fund_manager(self, data):
        for d in data:
            message = f"【{d['基金经理']}】{d.get('基金经理简介', '')}现任职{d['基金公司']}，从业{d['从业天数']}天。\n【管理基金】"
            for fund in d['管理基金类型']:
                message += f"\n[{fund['基金类型']}] 超过{fund.get('基金经理评分', '--')}%同类型基金经理，" +\
                           f"取得了年化收益{fund.get('历史年化收益', '--')}%的收益，最大回撤控制在{fund['历史最大回撤']}%。" +\
                           f"代表作[{fund['代表作']}]"
            message += f"\n点击查看：{self.parse_url(d['基金经理详情链接'])}"
            self.reply += '\n' + message + '\n'

    def parse_index_market(self, data):
        for key in ('A股指数', '沪深300', '中证500', '创业板指', '标普500', '纳斯达克100', '恒生指数'):
            d = data[key]
            if key == 'A股指数':
                key = 'A股'

            message = f"【{key}】\n近1日涨幅{d['近一日收益率']}%，近1周涨幅{d['近一周收益率']}%，近1月涨幅{d['近一月收益率']}%，" +\
                      f"近3月涨幅{d['近三月收益率']}%，近6月涨幅{d['近半年收益率']}%，近1年涨幅{d['近一年收益率']}%\n" +\
                      f"点击查看：{self.parse_url(d['指数详情链接'])}"
            self.reply += '\n' + message + '\n'

    def parse_low_market(self, data):
        for key in ('PE', 'PB'):
            for d in data[f'{key}低估指数']:
                message = f"【{d['指数名称']}】\n{key}百分位：{d['低估百分位']}%" +\
                          f"点击查看：{self.parse_url(d['指数详情链接'])}"
                self.reply += '\n' + message + '\n'

    def parse_sector_market(self, data):
        sep = '\n' if len(data) == 1 else '，'
        for d in data[:5]:
            message = f"【{d['板块名称']}】\n近1周涨幅{d['近一周收益率']}%{sep}近1月涨幅{d['近一月收益率']}%{sep}" +\
                      f"近3月涨幅{d['近三月收益率']}%{sep}近6月涨幅{d['近半年收益率']}%{sep}近1年涨幅{d['近一年收益率']}%。\n" +\
                      f"点击查看：{self.parse_url(d['板块详情链接'])}\n" +\
                      f"代表基金[{d.get('代表基金', '--')}]"
            self.reply += '\n' + message + '\n'

    def parse_single(self, data):
        self.reply += '您可以{}说：'.format('@我之后' if self.be_at else '')
        for d in data:
            self.reply += '\n' + self.parse_url(d['value'])

    def parse_card(self, message_detail, data):
        if message_detail == 'FundBase':
            self.parse_fund([data])

        elif message_detail == 'FundList':
            self.parse_fund(data)

        elif message_detail == 'FundHold':
            self.parse_fund_position(data)

        elif message_detail == 'FundProfit':
            self.parse_fund_market(data)

        elif message_detail == 'FundManager':
            self.parse_fund_manager([data])

        elif message_detail == 'FundManagerList':
            self.parse_fund_manager(data)

        elif message_detail == 'IndexMarketList':
            self.parse_index_market(data)

        elif message_detail == 'IndexList':
            self.parse_low_market(data)

        elif message_detail == 'SectorInfo':
            self.parse_sector_market([data])

        elif message_detail == 'SectorList':
            self.parse_sector_market(data)

        elif message_detail == 'BaseCard':
            self.parse_single(data)

    #########
    # Parse #
    #########

    def parse_prefix_message(self, prefix_message):
        if not prefix_message:
            return

        self.reply = prefix_message

    def parse_data(self, message_type, message_detail, data):
        """
        card - FundBase         基金卡片, data 为 dict
        card - FundList         基金卡片, horizontal, data 为 list
        card - FundHold         基金持仓卡片, data 为 dict
        card - FundProfit       基金收益卡片, data 为 dict
        card - FundManager      基金经理卡片, data 为 dict
        card - FundManagerList  基金经理卡片, horizontal, data 为 list
        card - IndexMarketList  主要指数行情卡片, horizontal, data 为 dict
        card - IndexList        低估指数行情卡片, horizontal, data 为 dict
        card - SectorInfo       行业板块行情卡片, data 为 dict
        card - SectorList       行业板块行情卡片, horizontal, data 为 list
        card - BaseCard         带可点击项的内容, data 为 list
        message - link          适用对话结尾显示的链接, data 为 dict
        message - text          适用对话中的纯文本内容, data 为 string
        message - mini          小程序报错提示, data 为 string
        message - error         对话图报错提示, data 为 string
        """
        if self.reply:
            self.reply += '\n'

        if message_type == 'message':
            self.parse_message(message_detail, data)
        elif message_type == 'card':
            self.parse_card(message_detail, data)

    def parse_jump_url(self, jump_url):
        if not jump_url:
            return

        if self.reply:
            self.reply += '\n'

        self.reply += jump_url['key'] + ':\n' + self.parse_url(jump_url['value'])

    def parse_quick_reply(self, quick_reply):
        if not quick_reply:
            return

        if self.reply:
            self.reply += '\n'

        self.reply += '—' * 12 + '\n您可以{}说：\n'.format('@我之后' if self.be_at else '')

        for reply in quick_reply:
            self.reply += reply['value'] + '\n'

    def parse_response(self):
        if not self.data:
            return RsvpResponse(self.stages, self.wechat_group_id, self.be_at).parse_stages()

        self.parse_prefix_message(self.data.get('prefix_message'))

        self.parse_data(self.data['type'], self.data['detail'], self.data.get('data'))

        self.parse_jump_url(self.data.get('jump_url'))
        self.parse_quick_reply(self.data['quick_reply'])

        return self.similarity, self.reply, self.start_miniprogram, self.data

