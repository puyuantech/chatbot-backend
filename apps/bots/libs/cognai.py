

def generate_cognai_response(output, stock_name):
    if not output:
        return {"status": -1}

    return {
        "stage": [
            {
                "text": {
                    "plainText": [
                        output
                    ],
                    "text": [
                        output
                    ],
                    "isRich": False
                }
            },
            {
                "quickReplies": {
                    "quickReplies": [
                        {
                            "text": f"重仓{stock_name}的基金有哪些",
                            "postback": f"重仓{stock_name}的基金有哪些？"
                        },
                        {
                            "text": "我要投资",
                            "postback": "我要投资。"
                        },
                        {
                            "text": "推荐基金",
                            "postback": "给我推荐基金。"
                        },
                        {
                            "text": "搜索基金",
                            "postback": "我想搜索基金。"
                        },
                        {
                            "text": "特色榜单",
                            "postback": "我想看看特色榜单。"
                        },
                        {
                            "text": "个性化推荐",
                            "postback": "为我进行个性化推荐。"
                        },
                        {
                            "text": "我的画像",
                            "postback": "查看我的画像。"
                        }
                    ]
                }
            }
        ],
        "status": 0
    }

