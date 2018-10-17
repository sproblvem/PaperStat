from bs4 import BeautifulSoup
import requests
import json
import random
import time

year = "2018"
config = {
    "2016": {
        "paperItem": "Poster",
        "DL": ["1", "7"],
        "RL": ["40", "50"],
        "BY": ["17", "43", "48"]
    },
    "2017": {
        "paperItem": "Poster",
        "DL": ["64", "100", "71", "64", "175", "118", "66", "168", "79", "181", "114", "63"],
        "RL": ["138", "87"],
        "BY": ["17", "105", "48", "99", "129", "170"]
    },
    "2018": {
        "paperItem": "Poster",
        "DL": ["https://nips.cc/Conferences/2018/Schedule?q=Deep+learning", "https://nips.cc/Conferences/2018/Schedule?q=Neural+network"],
        "RL": ["https://nips.cc/Conferences/2018/Schedule?q=reinforcement+learning"],
        "BY": ["https://nips.cc/Conferences/2018/Schedule?q=Bayesian", "https://nips.cc/Conferences/2018/Schedule?q=Gaussian+Processes", "https://nips.cc/Conferences/2018/Schedule?q=Statistical+Learning"]
    }
}


paper_author_list = {}
author_institute = {}
paper_session_list = {}

def get_result(base_url, session):
    paperList = []
    req = requests.get(base_url)
    base_html = BeautifulSoup(req.text, 'html.parser')
    def isPaper(tag):
        if tag.has_attr("onclick"):
            if tag["onclick"].startswith("showDetail"):
                if config[year]["paperItem"] in tag.div["class"]:
                    paperList.append("https://nips.cc/Conferences/" + year + "/Schedule?showEvent=" + tag["onclick"][11:-1])
        return False
    base_html.find_all(isPaper)

    speakerList = []
    def isAuthor(tag):
        if tag.has_attr("onclick"):
            if tag["onclick"].startswith("showSpeaker"):
                speakerList.append("https://nips.cc/Conferences/" + year + "/Schedule?showSpeaker=" + tag["onclick"][13:-3])
        return False

    def isNone(s):
        if s == '' or s == '\n':
            return False
        return True

    for paperUrl in paperList:
        speakerList.clear()
        req = requests.get(paperUrl)
        paper_html = BeautifulSoup(req.text, 'html.parser')
        paperName = paper_html.find("div", attrs={'class': 'maincardBody'}).text
        authors = paper_html.find("div", attrs={"class": "maincardFooter"}).text.split(" · ")
        paper_author_list[paperName] = authors
        if paperName not in paper_session_list.keys():
            paper_session_list[paperName] = []
        if session not in paper_session_list[paperName]:
            paper_session_list[paperName].append(session)
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
        break

if year == "2018":
    for session in ["DL", "RL", "BY"]:
        for base_url in config[year][session]:
            get_result(base_url, session)
else:
    for session in ["DL", "RL", "BY"]:
        base_url = "https://nips.cc/Conferences/" + year + "/Schedule?bySubject="
        for i in config[year][session]:
            base_url += "&selectedSubject=" + i
        get_result(base_url, session)


with open('nips_' + year + '.json', 'w') as file_object:
    json.dump([paper_author_list, paper_session_list, author_institute], file_object)