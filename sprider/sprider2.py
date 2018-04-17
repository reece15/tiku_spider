# coding:utf-8

import requests
import json
import time
from multiprocessing.dummy import Pool
from Queue import Queue
import threading


url="https://www.zujuan.com/question/list"


headers = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
 'referer':'https://www.zujuan.com/',
 'accept-language':"zh-CN,zh;q=0.8,en;q=0.6",
 'accept-encoding':'gzip, deflate, sdch, br',
 'accept':"application/json, text/javascript, */*; q=0.01"
}

queue = {}

def get_cate_ids():
    ids = []
    with open("cate.txt", "rt") as fp:
        for line in fp:
            grade = json.loads(line)
            for category, name in grade["categories"].items():
                yield category
                ids.append(category)

def init_page(ids):
    for id in ids:
        page = get_page(id)
        for p in xrange(1, page+1,1):
            yield {"cate_id":id, "page": p}


def get_page(id):
    data = get(1, id)
    total = data["total"]
    return int(round(total*1.0/len(data["ids"])))


def get_to_q(c):
    page, cate_id = c["page"], c["cate_id"]
    queue[cate_id].put(get(page, cate_id))


def get(page, cate_id):
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
    params.update({
        "categories":cate_id,
        "page":page,
        "_": int(time.time())
    })
    print "Cate:{} Page:{} start".format(cate_id, page)
    r = requests.get(url, params=params, headers=headers)
    data = json.loads(r.content)
    print "Cate:{} Page:{} end, ids:{}".format(cate_id,page, data["ids"])
    return data

def save(cate_id):
    with open("data\{}.txt".format(cate_id), "wt") as f:
        while True:
            q = queue[cate_id]
            while q.qsize():
                item = q.get()
                f.write(json.dumps(item)+"\n")
                f.flush()

if __name__ == "__main__":

    ids = list(get_cate_ids())
    pages = init_page(ids)

    for id in ids:
        queue[id] = Queue()
        t = threading.Thread(target=save, args=(id,))
        t.start()
    pool = Pool(20)


    pool.map(get_to_q, pages)
    print "Done"
