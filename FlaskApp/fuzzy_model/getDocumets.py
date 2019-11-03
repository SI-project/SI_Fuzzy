import re
import json

def getText():
    data = ""
    with open('./07.topics.901-950','r') as fd:
        data += fd.read()
    with open('./07.feed-distillation-topics.951-995','r') as fd:
        data += fd.read()
    return data

def getTops(text):
    tops = re.compile(r'<top>(.*?)</top>',re.S)
    list_tops = tops.findall(text)
    return list_tops

def getTags(list_top):
    titles = []
    nums = []
    descs = []
    narrs = []
    titles_exp = re.compile(r"<title>.*</title>",re.S)
    nums_exp = re.compile(r"<num>.*</num>",re.S)
    descs_exp = re.compile(r"<desc>.*</desc>",re.S)
    narrs_exp = re.compile(r"<narr>.*</narr>",re.S)
    for top in list_top:
        t = titles_exp.findall(top)[0]
        t = re.sub(r"(<title>)|(</title>)", "", t)
        titles.append(t)
        t = nums_exp.findall(top)[0]
        t = re.sub(r"(<num>)|(</num>)", "", t)
        nums.append(t)
        t = descs_exp.findall(top)[0]
        t = re.sub(r"(<desc>)|(</desc>)", "", t)
        descs.append(t)
        t = narrs_exp.findall(top)[0]
        t = re.sub(r"(<narr>)|(</narr>)", "", t)
        narrs.append(t)
    return titles, nums, descs, narrs

def save_json():
    list_to_save = []
    with open("./corpus.json", 'w+') as corpus:
        text = getText()
        l = getTops(text)
        titles,nums,descs,narrs = getTags(l)
        for i in range(len(titles)):
            obj = {
                'title': titles[i],
                'num': nums[i],
                'desc': descs[i],
                'narr' : narrs[i]
            }
            list_to_save.append(obj)
        json.dump(list_to_save, corpus)

save_json()