# coding:utf-8

import requests
import json
import time


url="https://www.zujuan.com/question/list"
params = {
    "categories":91881,
    "question_channel_type":1,  # 题型 单选1  填空4  计算题5 解答6  作图25  综合28
    "difficult_index":"",  # 难度   1容易   2中等   3难
    "exam_type": "",     # 试题类型　　１中考 2 常考 7 模拟
    "kid_num":"",   # 多少个知识点  1  2  3
    #"grade_id%5B%5D":0,  # 几年级的 7  8  9
    #"grade_id%5B%5D":8,
    "sortField":"time",  # 排序  count 组卷次数  time 时间
    "page":1,  #   页码
    "_":1523599236402,  # 时间戳
}

headers = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
 'referer':'https://www.zujuan.com/',
 'accept-language':"zh-CN,zh;q=0.8,en;q=0.6",
 'accept-encoding':'gzip, deflate, sdch, br',
 'accept':"application/json, text/javascript, */*; q=0.01"
}

total = 99999999
page = 1
cnt = 0
with open("data2.txt", "wt") as f:
    while True and cnt < total:

        params.update({
            "page":page,
            "_": int(time.time())
        })
        print "Page:{} start".format(page)
        r = requests.get(url, params=params, headers=headers)
        data = json.loads(r.content)

        f.write(r.content+"\n")
        print "Page:{} end, ids:{}".format(page, data["ids"])
        total = int(data["total"])
        cnt += len(data["ids"])
        page += 1

