
from bases.viewhandler import ApiViewHandler
from extensions.cognai import CognaiBot

from .libs.cognai import generate_cognai_response


class CognaiDialogAPI(ApiViewHandler):

    def get(self):
        """查询用户对话量分布统计, 获取 Cognai 回复"""
        cognai = CognaiBot.get_cognai_bot()
        resp = cognai.get_response(self.input.q)

        output = stock_name = ''
        if resp and resp.get('code') == 0:
            answer = resp.get('answer', {})
            cognai_answer_series = answer.get('series')
            cognai_answer_data = answer.get('data')

            if cognai_answer_series:
                for series in cognai_answer_series:
                    if series.get('name') and series.get('data'):
                        output += f'{series.get("name")}：\n'
                        stock_name = stock_name or series.get("name").split('-')[0]
                    for item in series.get('data', []):
                        output += f'{item[0]}: {round(item[1] * 100) / 100.0}\n'

            elif cognai_answer_data:
                for data in cognai_answer_data:
                    if data.get('index') and data.get('short_name'):
                        output = output or '为您找到下列数据：\n'
                        stock_name = stock_name or data.get("short_name")
                        output += f'{data.get("short_name")}({data.get("index")})\n'

        return generate_cognai_response(output, stock_name)

