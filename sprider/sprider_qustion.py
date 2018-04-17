# coding:utf-8

import requests
import json
import time
import re
from test import get_code
import os
import threading

url="https://www.zujuan.com/question/detail-{}.shtml"

headers = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
 'referer':'https://www.zujuan.com/',
 'accept-language':"zh-CN,zh;q=0.8,en;q=0.6",
 'accept-encoding':'gzip, deflate, sdch, br',
 'accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

from Queue import  Queue
from multiprocessing.dummy import Pool


queue = Queue()
pool = Pool(20)

re_answer = re.compile(r'"answer":"([^"]+)"')

def get(item):
    id = item["question_id"]
    t = item["question_channel_type"]
    print id

    if t != "1":
        return
    r = requests.get(url.format(id), headers=headers)
    answer = re_answer.findall(r.content)
    print answer
    if answer:
        r = requests.get(answer[0], headers=headers)
        ans = get_code(r.content)

        d = {
            "id": id,
            "t": t,
            "answer": ans,
            "answer_url": answer,
        }
        s = json.dumps(d)
        print s
        queue.put(s)
    else:
        print "Id:{} is err!".format(id)


def gen():
    a = []
    ps = os.listdir("data")
    for p in ps:
        with open("data\{}".format(p)) as f:
            for line in f:
                data = json.loads(line)
                for item in data["data"][0]["questions"]:
                    yield item
                    a.append(item)

def save():
    with open("ans_all.txt", "wt") as f:
        while True:
            while queue.qsize():
                item = queue.get()
                f.write(item+"\n")

t = threading.Thread(target=save)
t.start()
pool.map(get, gen())
print "Done"

