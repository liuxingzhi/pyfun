import requests
from requests.exceptions import *
from googletrans import Translator
import bs4
from bs4 import BeautifulSoup

apikey = "eec9ea27b7184108a9ac7df7ad9089e7"
tuling_url = "http://openapi.tuling123.com/openapi/api"


def google_translate(content):
    try:
        translator = Translator(timeout=3)
        content_info = translator.detect(content)
        print(content_info)
        result = None
        if content_info.lang == "en":
            result = translator.translate(content, dest="zh-CN").text
        elif content_info.lang == "zh-CN":
            result = translator.translate(content, dest="en").text
        else:
            result = translator.translate(content, dest="zh-CN").text
            result += "\n" + translator.translate(content, dest="en").text
        result += "\n" + "  //by google translation"
        return result
    except ConnectionError as e:
        print("连不上google服务器")
        return "连接google失败，貌似主人忘了接VPN？"
    except:
        print("google其他异常")
        return "google服务异常"


def tuling_response(dialog):
    data = {
        'key': apikey,
        'info': dialog,
    }
    try:
        result = requests.post(tuling_url, data=data).json()
        return result['text']
    except:
        print("图灵机的异常")
        return "哎呀，出错了呢，看来我还需要改进"


def haici_lookup(phrase):
    try:
        haici_url = "http://dict.cn/"
        haici_url += phrase.replace(" ", "%20")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0 Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}
        r = requests.get(haici_url, headers=headers, timeout=5)
        print(r.status_code)
        r.raise_for_status()
        r.encoding = "UTF-8"
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        meaning = ""
        tags = soup.body.find(name="div", attrs={'class': 'basic clearfix'}).find("li").children
        for tag in tags:
            if isinstance(tag, bs4.element.Tag):
                meaning += tag.text
        return meaning
    except (HTTPError, Timeout) as e:
        print("网络异常，连接超时")
        return "网络异常"
    except AttributeError as e:
        print("单词不存在")
        return "没有找到与此相符的结果"
    except:
        print("海词词典的其他异常")
        return "哎呀，出错了呢，看来我还需要改进"
