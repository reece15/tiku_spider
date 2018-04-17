# coding:utf-8
import requests
from pyquery import PyQuery as pq
import re
import json

headers = {
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
 'referer':'https://www.zujuan.com/',
 'accept-language':"zh-CN,zh;q=0.8,en;q=0.6",
 'accept-encoding':'gzip, deflate, sdch, br',
 'accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

base_cate = [
{"name":"七年级上册","url":"/question?categories=10166&bookversion=10430&nianji=10166&chid=3&xd=2"},
{"name":"七年级下册","url":"/question?categories=10167&bookversion=10430&nianji=10167&chid=3&xd=2"},
{"name":"八年级上册","url":"/question?categories=10168&bookversion=10430&nianji=10168&chid=3&xd=2"},
{"name":"八年级下册","url":"/question?categories=10169&bookversion=10430&nianji=10169&chid=3&xd=2"},
{"name":"九年级上册","url":"/question?categories=10170&bookversion=10430&nianji=10170&chid=3&xd=2"},
{"name":"九年级下册","url":"/question?categories=10171&bookversion=10430&nianji=10171&chid=3&xd=2"}]
# base_cate = ["/question?categories=10166&bookversion=10430&nianji=10166&chid=3&xd=2",
#  "/question?categories=10167&bookversion=10430&nianji=10167&chid=3&xd=2",
#  "/question?categories=10168&bookversion=10430&nianji=10168&chid=3&xd=2",
#  "/question?categories=10169&bookversion=10430&nianji=10169&chid=3&xd=2",
#  "/question?categories=10170&bookversion=10430&nianji=10170&chid=3&xd=2",
#  "/question?categories=10171&bookversion=10430&nianji=10171&chid=3&xd=2"]
#  $("a:contains(年级):contains(册)").map(function(){return $(this).attr("href");})
#  $("a:contains(年级):contains(册)").each(function(){document.write(JSON.stringify({"name": $(this).text(),"url":$(this).attr("href")})+",");})




url="https://www.zujuan.com"



re_cate = re.compile(r'categories=(\d+)&')

with open("cate.txt", "wt") as f:
    for i in base_cate:
        r = requests.get(url + i["url"], headers=headers)
        t = r.content
        doc = pq(t)
        categories = {
        }
        for item in doc("#J_Tree a"):
            item = pq(item)
            id = re_cate.findall(item.attr("href"))[0]
            categories[id] = item.text()
            print id, item.text()
        i["categories"] = categories

        f.write(json.dumps(i)+"\n")

