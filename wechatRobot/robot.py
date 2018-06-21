import itchat
from itchat.content import *
from crawlers import *

user_dict = {}
introduction = "你好,我是Abel的微信机器人艾伯. 现在的功能有:\n1.查单词(#开头)\n2.翻译($开头)\n3.聊天"
keywords = ["说明", "介绍", "你是谁"]
my_id = None


@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
    text = msg['Text']
    user_id = msg['FromUserName']
    if user_id == my_id:
        return
    print("msg", text)
    print(msg)
    print("username", msg['FromUserName'])
    result = None
    if user_dict[user_id] == 0:
        itchat.send(introduction, user_id)
        return
    elif text[0] == '#':
        result = haici_lookup(text[1:])
    elif text[0] == '$':
        result = google_translate(text[1:])
    else:
        head = text[:4]
        for keyword in keywords:
            if keyword in head:
                itchat.send(introduction, user_id)
                return
        else:
            result = tuling_response(text)
    user_dict[user_id] += 1
    print("返回结果", result)
    itchat.send(result, user_id)


def main():
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends()
    global my_id
    for index, user in enumerate(friends):
        id = user.get("UserName", "notexist")
        if index == 0:
            my_id = id
        user_dict[id] = 0
    print(user_dict)
    itchat.run()


if __name__ == '__main__':
    main()
