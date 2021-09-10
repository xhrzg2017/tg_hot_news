# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     demo.py
   Description :   网络热搜 tg机器人
   Author :       xhrzg2017
   date：          2021/9/9
-------------------------------------------------
   Change Activity: 2021/9/9:
-------------------------------------------------
"""
__author__ = 'xhrzg2017'

import requests, telegram, time, parsel, re
from datetime import datetime, timedelta, timezone
from lxml import etree

notes = ""

tg_id = input("TGid：")  # TG@userinfobot可查询id，不使用tg推送则github不填TGID 留空
tg_token = '1984453979:AAHcMj_ctfgMnH3WvHFo0iZEspigSWLKY5k'  # 此值默认不用修改


# print(tg_id[:3] + '****' + tg_id[7:])

def baidu():
    global notes
    print('百度热搜TOP 10')
    notes += '百度热搜TOP 10\n\n'
    TOP = 0
    headers = {
        "Host": "top.baidu.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42'
    }
    url = 'https://top.baidu.com/board?tab=realtime'
    response = requests.get(url=url, headers=headers)
    # print(response.text)
    selector = parsel.Selector(response.text)
    lis = selector.css('.category-wrap_iQLoo')[:10]
    # print(lis)
    for li in lis:
        title = li.css('.c-single-text-ellipsis::text').get()
        href = li.css('.category-wrap_iQLoo a::attr(href)').get()

        if title == ' ':
            headers1 = {
                "Host": "www.baidu.com",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42'
            }
            response2 = requests.get(url=href, headers=headers1).text
            # print(response2)
            title = re.findall(r'<title>(.*?)_百度搜索', response2)[0]
            # print(title)
            TOP += 1
            # print('TOP' + str(TOP), title, href)

            text = 'TOP ' + str(TOP) + '<a href="' + href + '">' + ' ' + title + '</a>' +"\n"
            notes += text
        else:
            TOP += 1
            # print('TOP'+str(TOP),title,href)

            text = 'TOP ' + str(TOP) + '<a href="' + href + '">' + ' ' + title + '</a>' + "\n"
            notes += text
    print(notes)
    tgbot(tg_token, tg_id)


print(notes)
# 使用tgbot推送
def tgbot(tg_token, tg_id):
    if tg_id != '' and tg_token != '':

        bot = telegram.Bot(tg_token)
        utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        time = utc_dt.astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M')
        bj_time = utc_dt.astimezone(timezone(timedelta(hours=8)))
        if bj_time.hour < 12:
            print('早报')
            name = '早'
        elif bj_time.hour < 18:
            print('午报')
            name = '午'
        elif bj_time.hour < 23:
            print('晚报')
            name = '晚'
        elif bj_time.hour < 5:
            print('晨报')
            name = '晨'

        bot.send_message(chat_id=tg_id,
                         text=f'🎉网络热搜{name}报🎉：\n\n' + notes + '\n' + time + '\n\n' + '本消息由TGbot项目定时发送 \n https://github.com/xhrzg2017/tg_hot_news',
                         parse_mode=telegram.ParseMode.HTML)





if __name__ == '__main__':
    print("----------百度热搜开始尝试发送----------")
    baidu()
    print("----------百度热搜执行完毕----------")
