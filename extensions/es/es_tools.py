import pypinyin
import re


def chinese_to_pinyin(word, first=True):
    _res = []
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        if first:
            _res.extend(i[0][0])
        else:
            _res.extend(i)
    return _res


def build_pinyin(company_name):
    if not company_name:
        return ''
    company_name = company_name.lower()
    pinyin = re.sub("[a-zA-Z\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+", "", company_name)
    pinyin = ''.join(chinese_to_pinyin(pinyin))
    return pinyin


def modify_fund_manager(x):
    try:
        return x.split('\r\n')[-1].split('(')[0]
    except:
        return x


































