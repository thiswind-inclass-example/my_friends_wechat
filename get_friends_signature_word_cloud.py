import json
from collections import Counter
from typing import Dict, Iterator, List, Tuple

import itchat
from jieba.analyse import extract_tags
from pyecharts import options
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType

if __name__ == '__main__':

    # 登陆微信
    print('登陆微信 ...')
    itchat.auto_login(hotReload=True)
    itchat.dump_login_status()

    # 读取朋友列表
    print('读取朋友列表 ...')
    friends = itchat.get_friends(update=True)

    # 微信定义的朋友属性，其中很多并没有官方的解释
    attribute_list: List[str] = [
        'MemberList', 'Uin', 'UserName', 'NickName',
        'HeadImgUrl', 'ContactFlag', 'MemberCount',
        'RemarkName', 'HideInputBarFlag', 'Sex',
        'Signature', 'VerifyFlag', 'OwnerUin',
        'PYInitial', 'PYQuanPin', 'RemarkPYInitial',
        'RemarkPYQuanPin', 'StarFriend',
        'AppAccountFlag', 'Statues', 'AttrStatus',
        'Province', 'City', 'Alias', 'SnsFlag',
        'UniFriend', 'DisplayName', 'ChatRoomId',
        'KeyWord', 'EncryChatRoomId', 'IsOwner'
    ]

    # 保存用户属性用的空列表
    friend_list: List[Dict] = list()

    # 读取用户属性
    print('读取用户属性...')
    for one_friend in friends:
        one: Dict[str, str] = dict()
        for one_attr in attribute_list:
            one[one_attr] = one_friend[one_attr]
        friend_list.append(one)

    # 可选：把读到的属性存盘
    with open('friends_data.json', 'w') as file:
        json.dump(friend_list, file, ensure_ascii=False)

    # 保存关键词的空列表
    all_tag_list: List[str] = list()

    # 从用户属性列表里，读取所有的用户签名
    print('读取所有的用户签名...')
    signature_list: Iterator = (one['Signature'] for one in friend_list)
    signature_list = filter(lambda x: len(str(x).strip()) > 0,
                            signature_list)  # 过滤掉空的签名

    # 定义忽略的词
    ignore_word_list: Tuple = (
        '<', 'span', 'class', '=', '\"', '\'', 'emoji', '>', '<', '/', 'gt',
        'lt'
    )

    # 从签名当中抽取关键词
    print('从签名当中抽取关键词...')
    for sig in signature_list:
        tag_list: Iterator = extract_tags(sig)  # 抽取关键词
        tag_list = filter(lambda x: len(str(x).strip()) > 0, tag_list)  # 过滤空词
        tag_list = filter(  # 过滤汉字、英文字母、数字之外的字符
            lambda x:
            all(uchar >= '\u4E00' and uchar <= '\u9FA5' for uchar in x)
            or
            all(uchar >= '\u0030' and uchar <= '\u0039' for uchar in x)
            or
            all(
                (uchar >= '\u0041' and uchar <= '\u005A') or (
                        uchar >= '\u0061' and uchar <= '\u007A')
                for uchar in x)
            ,
            tag_list
        )
        tag_list = filter(lambda x: x not in ignore_word_list,
                          tag_list)  # 过滤忽略的单词
        all_tag_list += tag_list

    # 对关键词计数
    print('对关键词计数...')
    tag_counter: Counter = Counter(all_tag_list)

    # 生成词云数据
    words = [(key, tag_counter[key]) for key in tag_counter]

    # 创建词云
    print('创建词云...')
    tag_word_cloud: WordCloud = WordCloud()
    tag_word_cloud.add(
        '',
        words,
        word_size_range=[9, 60],
        shape=SymbolType.DIAMOND
    )
    tag_word_cloud.set_global_opts(title_opts=options.TitleOpts(
        title=f'{friend_list[0]["NickName"]}的朋友们的微信签名'))
    tag_word_cloud.render()

    print('done')
