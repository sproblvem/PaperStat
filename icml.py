from bs4 import BeautifulSoup
import requests
import json
import random
import time

year = "2018"
base_url = "https://icml.cc/Conferences/" + year + "/Schedule"
req = requests.get(base_url)
base_html = BeautifulSoup(req.text, 'html.parser')

config = {
    "2017": {
        "paperItem": "Talk",
    },
    "2018": {
        "paperItem": "Oral",
    }
}

paperList = []
paper_author_list = {}
author_institute = {}
paper_session_list = {}
def isPaper(tag):
    if tag.has_attr("onclick"):
        if tag["onclick"].startswith("showDetail"):
            if config[year]["paperItem"] in tag.div["class"]:
                paperList.append("https://icml.cc/Conferences/" + year + "/Schedule?showEvent=" + tag["onclick"][11:-1])
    return False
base_html.find_all(isPaper)

speakerList = []
def isAuthor(tag):
    if tag.has_attr("onclick"):
        if tag["onclick"].startswith("showSpeaker"):
            speakerList.append("https://icml.cc/Conferences/" + year + "/Schedule?showSpeaker=" + tag["onclick"][13:-3])
    return False

def isNone(s):
    if s == '' or s == '\n':
        return False
    return True

for paperUrl in paperList:
    speakerList.clear()
    req = requests.get(paperUrl)
    paper_html = BeautifulSoup(req.text, 'html.parser')
    info_div = paper_html.find("div", attrs={'id': 'maincard_' + paperUrl.split("=")[-1]})
    paperName = info_div.find("div", attrs={"class": "maincardBody"}).text
    authors = info_div.find("div", attrs={"class": "maincardFooter"}).text.split(" · ")
    paper_author_list[paperName] = authors
    sessionName = info_div.find_all("div", attrs={"class": "pull-right maincardHeader maincardType"})[1].a.text
    sessionName = ' '.join(list(filter(isNone, sessionName.split(" "))))
    if paperName not in paper_session_list.keys():
        paper_session_list[paperName] = []
    if sessionName not in paper_session_list[paperName]:
        paper_session_list[paperName].append(sessionName)
    paper_html.find_all(isAuthor)
    for authorUrl in speakerList:
        req = requests.get(authorUrl)
        author_html = BeautifulSoup(req.text, 'html.parser')
        tag = author_html.find("div", attrs={"class": "maincard Remark col-sm-12"})
        author = tag.h3.text
        institute = tag.h4.text
        author_institute[author] = institute
    time.sleep(random.random())
    print(paperName)

with open('icml_' + year + '.json', 'w') as file_object:
    json.dump([paper_author_list, paper_session_list, author_institute], file_object)