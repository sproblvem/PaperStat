import numpy as np
import random
import argparse
import pickle
import os
import copy
from enum import Enum
from html.parser import HTMLParser

class Session(Enum):
    RL = 'Reinforcement Learning'
    BY = 'Statistical Learning, Bayesian, Gaussian Processes'
    DL = 'Deep Learning, Neural network'

class Nation(Enum):
    china = 'china'
    usa = 'usa'

class PaperStat(object):
    def __init__(self, **kwargs):
        self.nations = {"China", "USA"}
        self.sessions = {"Machine Learning", "Reinforcement Learning"}
        self.name2session = {"ML" : "Machine Learning", "RL" : "Reinforcement Learning"}
        self.people2nation = {"Jun Zhu" : Nation.china, "Micheal Jordan" : Nation.usa}
        self.people2affi = {"Jun Zhu" : Nation.china, "Micheal Jordan" : Nation.usa}
        self.affi2nation = {"Tsinghua University" : Nation.china, "MIT" : Nation.usa}

    def show(self):
        print(Session)
        print(self.sessions)
        print(type(self.sessions))
        print(self.name2session)
        print(type(self.name2session))
        print(self.people2nation)
        print(type(self.people2nation))

paper_counter = 0
paper_id = 0
current_session = ""
paper_dict = {}
author = ""
get_author = False
author_depth = 0
depth = 0

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global paper_counter, paper_id, current_session, get_author, depth, author_depth, author
        if tag == "li":
            paper_counter += 1
        if tag == "h3" and attrs:       #   the name of current session in tag h3 and id attr
            current_session = attrs[0][1]
            current_session = current_session.replace("Wednesday", "")
            current_session = current_session.replace("Monday", "")
        if tag == "span":
            if len(attrs) >= 2 and attrs[1][0] == "id":
                paper_id = attrs[1][1]
            if attrs and attrs[0][1] == "authors":
                author_depth = depth
                get_author = True
                author = ""
        if tag == "i" and get_author:
            author += ";"
        depth += 1

    def handle_endtag(self, tag):
        global depth, get_author, paper_id, paper_dict, author, current_session
        if tag == "span":
            get_author = False
            paper_dict[paper_id] = [current_session, author.strip()]
        depth -= 1

    def handle_data(self, data):
        global get_author, author, author_depth
        if get_author:
            author += data


def main():
    # https://icml.cc/Conferences/2016/index.html%3Fp=1839.html
    file = open("icml2016.html", "r")
    #file = open("test.html", "r")
    icml2016 = file.read()
    #print(icml2016)

    #ps = PaperStat();
    #ps.show();
    parser = MyHTMLParser()
    parser.feed(icml2016)

    for k, v in paper_dict.items():
        print(k, v)
    print("ICML 2016 paper number : ", len(paper_dict.items()))

if __name__ == '__main__':
    main()
