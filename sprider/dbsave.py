# coding:utf-8


import MySQLdb
import json
import load_images

conn = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='exam', charset='utf8')





def load_unit():
    with open("cate.txt", "rt") as f:
        for line in f:
            cates = json.loads(line)
            for cate in cates["categories"].values():
                cursor = conn.cursor()
                effect_row = cursor.execute(u"insert into unit (book,unit,unit_index,grade) VALUES ('{book}','{unit}',{unit_index},'{grade}')".format(book=u"人教版", unit=cate, unit_index=1, grade=cates["name"]))
                conn.commit()
                cursor.close()


def select_unit():
    cursor = conn.cursor()
    cursor.execute(u"select id,unit from `unit`")
    results = cursor.fetchall()
    mapping = {}
    for row in results:
        mapping[row[1]]=row[0]
    conn.commit()
    cursor.close()

    res = {}
    with open("cate.txt", "rt") as f:
        for line in f:
            cates = json.loads(line)
            for cate_id,cate_name in cates["categories"].items():
                res[cate_id] = mapping[cate_name]
    return res


def load_ans():
    ans = {}
    with open("ans_all.txt", "rt") as f:
        for line in f:
            a = json.loads(line)
            ans[a["id"]] = a["answer"]
    return ans

def load_questions_and_answer(unit_mapping, ans):
    import os
    import datetime
    index = 0
    cursor = conn.cursor()
    files = os.listdir("data")
    for file_index, file in enumerate(files):
        with open("data/{}".format(file), "rt") as f:
            unit_id = unit_mapping.get(file.split(".")[0])

            for line in f:
                q = json.loads(line)
                for ques in q["data"][0]["questions"]:
                    anss = ans.get(ques["question_id"])

                    if anss is not None:
                        anss = anss.strip()
                        if anss not in ["A", "B", "C","D"]:
                            anss = None
                    break_flag = False
                    if ques["options"] and isinstance(ques["options"], dict):
                        for option, val in ques["options"].items():
                            if val is None:
                                print "-"*100
                                break_flag = True
                                break
                            image_str=load_images.load_save(unit_id=unit_id, images_str=val)
                            if image_str is not None:
                                ques["options"][option] = image_str
                    if break_flag:
                        continue
                    question_text = load_images.load_save(unit_id=unit_id, images_str=ques["question_text"])
                    res = {
                        "exam_type": ques["exam_type"],
                        "kid_num": ques["kid_num"],
                        "difficult_index": ques["difficult_index"],
                        "qtype": ques["question_channel_type"],
                        "content": question_text if question_text else ques["question_text"],
                        "source":ques["question_source"],
                        "options": json.dumps(ques["options"]),
                        "answer": json.dumps({"option": anss}) if anss else "",
                        "unit_id": unit_id,
                        "join_time": datetime.datetime.now()
                    }

                    keys = list(res.keys())
                    res_keys = ",".join(keys)
                    res_values = map(lambda k:res[k],keys)
                    key_values = ",".join(["%s"]*len(keys))

                    sql = u"insert into question ({res_keys}) VALUES ({key_values})".format(**vars())
                    print file_index, index, sql
                    effect_row = cursor.execute(sql, res_values)
                    conn.commit()
                    index += 1
    cursor.close()

load_unit()
unit_mapping = select_unit()

load_images.run()
ans = load_ans()
load_questions_and_answer(unit_mapping, ans)
conn.close()

print "Done"
while "a" == raw_input():
    pass
