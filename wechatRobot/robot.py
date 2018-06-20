import itchat
from itchat.content import *
import requests
from googletrans import Translator

apikey = "eec9ea27b7184108a9ac7df7ad9089e7"
tuling_url = "http://openapi.tuling123.com/openapi/api"

count = 0
@itchat.msg_register(TEXT)
def text_reply(msg):
    text = msg['Text']
    print("msg", text)
    print(msg)
    print("username", msg['FromUserName'])
    result = None
    if text[0] == '#':
        result = google_translate(text[1:])
    else:
        global count
        count += 1
        if count <= 1:
            itchat.send("现在是Abel的机器人艾伯在和你对话", msg['FromUserName'])
        result = tuling_response(text)
    print("返回结果", result)
    itchat.send(result, msg['FromUserName'])


def google_translate(content):
    translator = Translator()
    content_info = translator.detect(content)
    print(content_info)
    result = None
    if content_info.lang == "en":
        result = translator.translate(content, dest="zh-CN").text
    elif content_info.lang == "zh-CN":
        result = translator.translate(content, dest="en").text
    else:
        result = translator.translate(content, dest="zh-CN").text
    result += "  //by google translation"
    return result


def tuling_response(dialog):
    data = {
        'key': apikey,
        'info': dialog,
    }
    try:
        result = requests.post(tuling_url, data=data).json()
        return result['text']
    except:
        return ""


def main():
    itchat.auto_login(hotReload=True)
    itchat.run()


if __name__ == '__main__':
    main()
