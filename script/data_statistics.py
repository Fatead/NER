#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: zhaocy
@Email: 19110240027@fudan.edu.cn
@Created: 2020/6/18
------------------------------------------
@Modify: 2020/6/18
------------------------------------------
@Description: 
"""
from definitions import DATA_DIR
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Stats:

    def __init__(self, sequence):
        # sequence of numbers we will process
        # convert all items to floats for numerical processing
        self.sequence = [float(item) for item in sequence]

    def sum(self):
        if len(self.sequence) < 1:
            return None
        else:
            return sum(self.sequence)

    def count(self):
        return len(self.sequence)

    def min(self):
        if len(self.sequence) < 1:
            return None
        else:
            return min(self.sequence)

    def max(self):
        if len(self.sequence) < 1:
            return None
        else:
            return max(self.sequence)

    def avg(self):
        if len(self.sequence) < 1:
            return None
        else:
            return sum(self.sequence) / len(self.sequence)

    def median(self):
        if len(self.sequence) < 1:
            return None
        else:
            self.sequence.sort()
            return self.sequence[len(self.sequence) // 2]

    def stdev(self):
        if len(self.sequence) < 1:
            return None
        else:
            avg = self.avg()
            sdsq = sum([(i - avg) ** 2 for i in self.sequence])
            stdev = (sdsq / (len(self.sequence) - 1)) ** .5
            return stdev

    def percentile(self, percentile):
        if len(self.sequence) < 1:
            value = None
        elif (percentile >= 100):
            sys.stderr.write('ERROR: percentile must be < 100.  you supplied: %s\n' % percentile)
            value = None
        else:
            element_idx = int(len(self.sequence) * (percentile / 100.0))
            self.sequence.sort()
            value = self.sequence[element_idx]
        return value

def analyze_sent_length(sent_length_list):
    x = []
    y = []
    se = pd.Series(sent_length_list)
    countDict = dict(se.value_counts())
    for key in countDict:
        x.append(key)  # x值
        y.append(countDict[key])  # y值
    plt.bar(x, y)  # 绘制柱状图
    plt.xlabel("句子长度")
    plt.ylabel("句子数目")
    plt.show()  # 显示柱状图
    # # 前两个默认就是True,rug是在最下方显示出频率情况，默认为False
    # sns.distplot(s, hist=True, kde=True, rug=False)
    # # shade表示线下颜色为阴影,color表示颜色是红色
    # sns.kdeplot(s, shade=True, color='r')
    # # 在下方画出频率情况
    # sns.rugplot(s)
    # plt.title(label='Scores Distribution Chart')
    # plt.show()
    # bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    # length_cut = pd.cut(s, bins, right=False)
    # length_counts = length_cut.value_counts()
    # print(length_counts)

if __name__ == '__main__':
    rf_path = DATA_DIR + '/train/sent_relation_train.txt'
    rf_name = open(rf_path, 'r', encoding='UTF-8')

    relation_id_list = []

    for line in rf_name:
        all_field = line.strip('\n').split('\t')
        sent_id = all_field[0]
        relation_id = all_field[1]

        relation_id_list.append(relation_id)

    se = pd.Series(relation_id_list)
    countDict = dict(se.value_counts())

    print("关系的频次:", countDict)

    rf_name.close()

# if __name__ == '__main__':
#     rf_path = DATA_DIR + '/train/sent_train.txt'
#     rf_name = open(rf_path, 'r', encoding='UTF-8')
#
#     sent_set = set()
#     name_set = set()
#     sent_length_list = []
#     name_list = []
#
#     for line in rf_name:
#         all_field = line.strip('\n').split('\t')
#         sent_id = all_field[0]
#         name1 = all_field[1]
#         name2 = all_field[2]
#         sent = all_field[3]
#
#         sent_set.add(sent)
#         name_set.add(name1)
#         name_set.add(name2)
#         sent_length_list.append(len(sent))
#         name_list.append(name1)
#         name_list.append(name2)
#
#     # sent_length_stats = Stats(sent_length_list)
#     # se = pd.Series(sent_length_list)
#     # countDict = dict(se.value_counts())
#     # name_stats = Stats(countDict.values())
#
#     # print("不重复的句子数目: ", len(sent_set))
#     # print("不重复的实体数目: ", len(name_set))
#     # print("句子长度最大值:", sent_length_stats.max())
#     # print("句子长度最小值:", sent_length_stats.min())
#     # print("句子长度中位数:", sent_length_stats.median())
#     # print("句子长度平均数:", sent_length_stats.avg())
#     # print("实体出现最大频次:", name_stats.max())
#     # print("实体出现中位数频次:", name_stats.median())
#     # print(countDict)
#
#     rf_name.close()
