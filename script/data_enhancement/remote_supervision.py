#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: zhaocy
@Email: 19110240027@fudan.edu.cn
@Created: 2020/6/22
------------------------------------------
@Modify: 2020/6/22
------------------------------------------
@Description: 
"""
from definitions import DATA_DIR
import re
import codecs


def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return para.split("\n")


if __name__ == '__main__':
    rf_sent_path = DATA_DIR + '/train/sent_train.txt'
    rf_relation_path = DATA_DIR + '/train/sent_relation_train.txt'
    rf_wiki_path = DATA_DIR + '/wiki_cn'
    wf_rs_sent_train_path = DATA_DIR + '/train/rs_sent_train.txt'
    wf_rs_sent_relation_path = DATA_DIR + '/train/rs_sent_relation.txt'
    rf_sent = open(rf_sent_path, 'r', encoding='UTF-8')
    rf_relation = open(rf_relation_path, 'r', encoding='UTF-8')
    rf_wiki = codecs.open(rf_wiki_path, 'r', encoding='UTF-8')
    wf_rs_sent_train = open(wf_rs_sent_train_path, 'w', encoding='UTF-8')
    wf_rs_sent_relation = open(wf_rs_sent_relation_path, 'w', encoding='UTF-8')

    src_sents = []
    src_relations = []
    wiki_sents = []

    for line in rf_sent:
        src_sents.append(line)
    for line in rf_relation:
        src_relations.append(line)

    wiki_data = rf_wiki.read()
    wiki_sents = cut_sent(wiki_data)

    TRAIN_SENT_ID = 287352
    for index, src_sent in enumerate(src_sents):
        if src_relations[index].strip('\n').split('\t')[1] != '0':
            name1 = src_sent.strip('\n').split('\t')[1]
            name2 = src_sent.strip('\n').split('\t')[2]
            for wiki_sent in wiki_sents:
                if name1 in wiki_sent and name2 in wiki_sent:
                    sent_id = "TRAIN_SENT_ID_" + '%06d' % TRAIN_SENT_ID
                    name1_id = sent_id + '_1'
                    name2_id = sent_id + '_2'
                    name1_pos = str([wiki_sent.find(name1), wiki_sent.find(name1) + len(name1)])
                    name2_pos = str([wiki_sent.find(name2), wiki_sent.find(name2) + len(name2)])
                    sent_line = sent_id + '\t' + name1 + '\t' + name1_id + '\t' + name1_pos + '\t' + name2 + '\t' + name2_id + '\t' + name2_pos + '\t' + wiki_sent
                    print(sent_line)
                    wf_rs_sent_train.write(str(sent_line))
                    relation_id = src_relations[index].strip('\n').split('\t')[1]
                    relation_line = sent_id + '\t' + relation_id
                    print(relation_line)
                    wf_rs_sent_relation.write(str(relation_line) + '\n')
                    TRAIN_SENT_ID = TRAIN_SENT_ID + 1
