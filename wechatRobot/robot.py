import itchat
from itchat.content import *
from crawlers import *
import re

"""key:id, value:对话次数"""
user_dialog_num = {}

"""key:id, value:nickname"""
user_nickname_dict = {}

introduction = "你好,我是Abel的微信机器人艾伯. 现在的功能有:\n1.查单词(直接输入)\n2.翻译句子(#开头)\n3.聊天"
keywords = ["说明", "介绍", "你是谁"]
my_id = None
pattern = re.compile("^[a-zA-z\s]+$")


@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
    text = msg['Text']
    user_id = msg['FromUserName']
    # if user_id == my_id:
    #     return
    print("收到消息", text)
    print(msg)
    print("来自", user_nickname_dict[user_id], user_id)
    result = None
    if user_dialog_num[user_id] == 0:
        result = introduction
    else:
        if pattern.match(text) is not None:
            result = haici_lookup(text)
        elif text[0] == '#':
            result = google_translate(text[1:])
        else:
            head = text[:4]
            for keyword in keywords:
                if keyword in head:
                    result = introduction
                    break
            else:
                result = tuling_response(text)
    user_dialog_num[user_id] += 1
    print("返回结果", result)
    itchat.send(result, user_id)
    return


def main():
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends()
    global my_id
    for index, user in enumerate(friends):
        id = user.get("UserName", "notexist")
        nickname = user.get("NickName")
        if index == 0:
            my_id = id
        user_dialog_num[id] = 0
        user_nickname_dict[id] = nickname
    # print(user_dialog_num)
    itchat.run()


if __name__ == '__main__':
    main()
