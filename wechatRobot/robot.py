import itchat
from itchat.content import *
from crawlers import *
import re

"""key:id, value:状态码
   0 关闭
   1 第一次见面
   >1 对话中，统计本次对话次数
   初始化是0
"""
user_status_dict = {}

"""key:id, value:nickname"""
user_nickname_dict = {}

introduction = "你好,我是Abel的微信机器人艾伯. 现在的功能有:\n查单词(直接输入)\n#开头翻译句子\n中文聊天\n你说‘开始’我会开始说话，你说‘停止’我就会停止"
keywords = ["说明", "介绍", "你是谁"]
my_id = None

"""检测英文单词或词组"""
english_phrase = re.compile("^[a-zA-z\s]+$")

"""检测是否#开头，允许#之前有空格"""
sharp_symbol_begin = re.compile("^[\s#]*#")

"""聊天经常出现?或??表示困惑,使用它匹配"""
confuse_pattern = re.compile("^[?\s]+$")

project_address = "https://github.com/liuxingzhi/pyfun/tree/master/wechatRobot"


@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
    try:
        text = msg['Text']
        sender_id = msg['FromUserName']
        receiver_id = msg['ToUserName']
        print("收到消息", text)
        print("来自", user_nickname_dict[sender_id], "发给", user_nickname_dict[receiver_id])

        """我发送的消息"""
        if sender_id == my_id:
            """检测特殊口令"""
            if text == "停止":
                user_status_dict[receiver_id] = 0
                return
            if text == "开始":
                user_status_dict[receiver_id] = 1

            """检测状态码"""
            if user_status_dict[receiver_id] == 0:
                print("接收方状态为关闭")
                return

            result = None
            if user_status_dict[receiver_id] == 1:
                result = introduction
            else:
                if english_phrase.match(text) is not None:
                    """查单词模块"""
                    result = haici_lookup(text)
                    if result == "没有找到与此相符的结果":
                        result = text
                elif sharp_symbol_begin.match(text):
                    """google翻译模块"""
                    query = re.sub(sharp_symbol_begin, "", text)
                    result = google_translate(query)
                else:
                    """关键词检测"""
                    head = text[:4]
                    for keyword in keywords:
                        if keyword in head:
                            result = introduction
                            break
                        # else:
                        #     result = tuling_response(text)
                        #     if result == "我不会说英语的啦，你还是说中文吧。":
                        #         result = google_translate(result)
            user_status_dict[receiver_id] += 1
            print("返回结果", result, "\n")
            itchat.send(result, receiver_id)
            return

        else:
            """对方发送的消息"""
            """检测特殊口令"""
            if text == "停止" or text == "结束":
                user_status_dict[sender_id] = 0
                return
            if text == "开始":
                if user_status_dict[sender_id] > 1:
                    itchat.send("你说，我在", sender_id)
                    return
                else:
                    user_status_dict[sender_id] = 1

            """检测状态码"""
            if user_status_dict[sender_id] == 0:
                print("接收方状态为关闭")
                return

            result = None
            if user_status_dict[sender_id] == 1:
                result = introduction
            else:
                if confuse_pattern.match(text) is not None:
                    result = "? + 1"
                elif text == "项目地址":
                    result = project_address
                elif english_phrase.match(text) is not None:
                    """查单词模块"""
                    result = haici_lookup(text)
                    if result == "没有找到与此相符的结果":
                        result = text

                elif sharp_symbol_begin.match(text):
                    """google翻译模块"""
                    query = re.sub(sharp_symbol_begin, "", text)
                    result = google_translate(query)

                else:
                    """图灵机器人回复模块"""
                    head = text[:4]
                    """关键词检测"""
                    for keyword in keywords:
                        if keyword in head:
                            result = introduction
                            break
                    else:
                        result = tuling_response(text)
                        if result == "我不会说英语的啦，你还是说中文吧。":
                            result = google_translate(result)
            user_status_dict[sender_id] += 1
            print("返回结果", result, "\n")
            itchat.send(result, sender_id)
    except:
        print("装饰器的异常")


def main():
    itchat.auto_login(hotReload=True)

    """填充用户字典"""
    friends = itchat.get_friends()
    global my_id
    for index, user in enumerate(friends):
        id = user.get("UserName")
        nickname = user.get("NickName")
        if index == 0:
            my_id = id
        user_status_dict[id] = 0
        user_nickname_dict[id] = nickname

    itchat.run()


if __name__ == '__main__':
    main()
