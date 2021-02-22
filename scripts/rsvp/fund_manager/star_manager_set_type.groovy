if (基金类型 == '债券') {
    another_fund_type = '股票'
} else {
    基金类型 = '股票'
    another_fund_type = '债券'
}

prefix_message = '基金掌舵者的能力往往决定了该只基金能否战胜市场。我们基于对历史业绩的量化分析为您推荐以下基金经理。\n'
prefix_message += '以下是【' + 基金类型 + '型】明星基金经理：'

quick_reply_key = another_fund_type + '明星基金经理'
quick_reply_value = '好的' + quick_reply_key + '有哪些？'
quick_reply = [['key': quick_reply_key, 'value': quick_reply_value]]