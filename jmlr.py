import urllib.request as request
from bs4 import BeautifulSoup

import io
import sys
import random
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

import re

# req = request.Request(url='https://dl.acm.org/citation.cfm?id=2946645&picked=prox&preflayout=flat', headers=headers)
req = request.Request(url='https://dl.acm.org/citation.cfm?id=3122009&picked=prox&preflayout=flat', headers=headers)
html = request.urlopen(req)
bs_obj = BeautifulSoup(html.read(), 'html.parser')
text_list = bs_obj.find_all("a")

pattern_paper = re.compile('citation.cfm\?id=[0-9]{7}')
pattern_author = re.compile('author_page.cfm\?id=[0-9]{11}')
root_path = 'https://dl.acm.org/'

paper_urls = []
for text in text_list:
    print(text_list)
    try:
        if re.fullmatch(pattern_paper, text.get('href')) is not None:
            paper_urls.append(text.get('href'))
    except Exception:
        pass
html.close()
print(len(paper_urls))

paper_list = []
paper_author_list = {}
author_institute = {}
paper_tag_list = {}
author_start_tag = 'PDF'
author_end_tag = 'archive'
topic_start_tag = '\nAuthor Tags\n'
topic_end_tag = 'Contact Us'
author_start = False
topic_start = False
pattern_us = re.compile('[A-Z]{2}')
institute_country = {}

for paper_url in paper_urls:
    print('Query ' + paper_url)
    req = request.Request(url=root_path+paper_url, headers=headers)
    html = request.urlopen(req)
    bs_obj = BeautifulSoup(html.read(), 'html.parser')
    text_list = bs_obj.find_all('h1', 'mediumb-text')
    title = text_list[0].get_text()
    paper_list.append(title)
    paper_author_list[title] = []
    paper_tag_list[title] = []

    text_list = bs_obj.find_all('a')
    institute_list = bs_obj.find_all('small')
    institute_list = [text.get_text() for text in institute_list]
    author_index = 0

    for text in text_list:
        if (text.get_text() != ''):
            if text.get_text() == author_end_tag:
                author_start = False
            if text.get_text() == topic_end_tag:
                topic_start = False
            if author_start and author_index < len(institute_list):
                author_or_institute = text.get_text()
                if author_or_institute not in institute_list:
                    author = author_or_institute
                    paper_author_list[title].append(author)
                    author_index += 1
                else:
                    institute = institute_list[author_index]
                    author_institute[author] = institute
                    if re.match(pattern_us, institute.split(',')[-1][1:]):
                        institute_country[institute] = 'America'
                    else:
                        institute_country[institute] = institute.split(',')[-1][1:]
            if topic_start:
                paper_tag_list[title].append(text.get_text())
            if text.get_text() == author_start_tag:
                author_start = True
            if text.get_text() == topic_start_tag:
                topic_start = True
    print(paper_author_list)
    print(paper_tag_list)
    print(author_institute)
    print(institute_country)
    html.close()
    time.sleep(random.random())
    sys.stdout.flush()

import json
json.dump([paper_author_list, paper_tag_list, author_institute, institute_country], open('jmlr-2018.json', 'w'))
