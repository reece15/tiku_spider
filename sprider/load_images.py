#coding:utf-8

import requests
from pyquery import PyQuery as pq
import os
import uuid
from Queue import Queue
import threading


headers = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
 'referer':'https://www.zujuan.com/',
 'accept-language':"zh-CN,zh;q=0.8,en;q=0.6",
 'accept-encoding':'gzip, deflate, sdch, br',
 'accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}


queue = Queue()


def load_save(unit_id, images_str, path="images"):
    if images_str.find("<img")==-1:
        return images_str
    doc = pq(images_str)

    dir = "{}/{}".format(path,unit_id)
    if not os.path.exists(dir):
        os.mkdir(dir)
    for img in doc("img"):
        href = pq(img).attr("src")
        if href.find("http")> -1:
            name = str(uuid.uuid1()).replace("-", "").upper()

            p = "{}/{}.png".format(dir, name)

            queue.put({
                "name": p,
                "href": href
            })


            pq(img).attr("src", "/"+p)
    return doc.html()


def download_save():
    while True:
        d = queue.get()
        href=d["href"]
        name = d["name"]
        r = requests.get(href, headers=headers)
        with open(name, "wb") as f:
            f.write(r.content)
        print queue.qsize(), name

def run():
    for i in range(10):
        t=threading.Thread(target=download_save)
        t.setDaemon(True)
        t.start()

if __name__ == "__main__":
    html = u'''S<sub>△</sub><sub>ADE</sub>+S<sub>△</sub><sub>BCE</sub>=<img class=\"mathml\" src=\"https://math.21cnjy.com/MathMLToImage?mml=%3Cmath+xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F1998%2FMath%2FMathML%22%3E%3Cmfrac%3E%3Cmn%3E1%3C%2Fmn%3E%3Cmn%3E2%3C%2Fmn%3E%3C%2Fmfrac%3E%3C%2Fmath%3E&key=18cdc087dc3a24f8d5a3a532b8735354\" style=\"vertical-align: middle;\">S<sub>▱</sub><sub>ABCD</sub>'''

    print load_save(23, html)

