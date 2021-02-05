if (ETF类型 == null) {
    ETF类型 = '场外'
}

if (ETF类型 == '场内') {
    another_etf_type = '场外'
} else {
    another_etf_type = '场内'
}

recommend_type = '指数型'

quick_reply_key = 指数 + another_etf_type + 'ETF'
quick_reply_value = quick_reply_key + '有哪些？'
quick_reply = [['key': quick_reply_key, 'value': quick_reply_value]]