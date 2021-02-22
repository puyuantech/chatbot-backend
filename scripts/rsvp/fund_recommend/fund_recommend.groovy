if (recommend_type == null) {
    recommend_type = '股票型'
}

response = [
    'type': 'card',
    'detail': 'FundList',
    'prefix_message': prefix_message,
    'jump_url': jump_url,
    'quick_reply': [],
    'data': 推荐基金.containsKey(recommend_type) ? 推荐基金[recommend_type] : []
]

if ( !quick_reply ) {
    quick_reply_type = true
    推荐基金.each { key, value ->
        if (key != recommend_type) {
            response.quick_reply.add(['key': key, 'value': key])
        }
    }
} else {
    quick_reply_type = false
    response.quick_reply = quick_reply
}