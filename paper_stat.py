import numpy as np
import random
import argparse
import pickle
import os
import copy
from enum import Enum

class Nation(Enum):
    china = 'china'
    usa = 'usa'

class PaperStat(object):
    def __init__(self, **kwargs):
        self.nations = {"China", "USA"}
        self.sessions = {"Machine Learning", "Reinforcement Learning"}
        self.name2session = {"ML" : "Machine Learning", "RL" : "Reinforcement Learning"}
        self.people2nation = {"Jun Zhu" : Nation.china, "Micheal Jordan" : Nation.usa}
        self.affiliation2nation = {"Tsinghua University" : Nation.china, "MIT" : Nation.usa}

    def show(self):
        print(self.sessions)
        print(type(self.sessions))
        print(self.name2session)
        print(type(self.name2session))
        print(self.people2nation)
        print(type(self.people2nation))

def main():
    ps = PaperStat();
    ps.show();

if __name__ == '__main__':
    main()
