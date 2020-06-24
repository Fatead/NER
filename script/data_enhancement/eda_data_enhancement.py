#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: zhaocy
@Email: 19110240027@fudan.edu.cn
@Created: 2020/6/21
------------------------------------------
@Modify: 2020/6/21
------------------------------------------
@Description: 
"""
from definitions import DATA_DIR

if __name__ == '__main__':
    rf_sent_path = DATA_DIR + '/train/sent_train.txt'
    rf_relation_path = DATA_DIR + '/train/sent_relation_train.txt'
    rf_eda_train_path = DATA_DIR + '/train/train_augmented.txt'
    wf_eda_sent_train_path = DATA_DIR + '/train/eda_sent_train.txt'
    wf_eda_sent_relation_path = DATA_DIR + '/train/eda_sent_relation.txt'
    rf_sent = open(rf_sent_path, 'r', encoding='UTF-8')
    rf_relation = open(rf_relation_path, 'r', encoding='UTF-8')
    rf_eda_train = open(rf_eda_train_path, 'r', encoding='UTF-8')
    wf_eda_sent_train = open(wf_eda_sent_train_path, 'w', encoding='UTF-8')
    wf_eda_sent_relation = open(wf_eda_sent_relation_path, 'w', encoding='UTF-8')

    eda_sents = []
    src_sents = []

    for line in rf_eda_train:
        eda_sents.append(line)
    for line in rf_sent:
        src_sents.append(line)

    TRAIN_SENT_ID = 1
    for line in eda_sents:
        relation = line.strip('\n').split('\t')[0]
        sent_id = "TRAIN_SENT_ID_" + '%07d' % TRAIN_SENT_ID
        new_line = sent_id + '\t' + relation
        TRAIN_SENT_ID = TRAIN_SENT_ID + 1
        wf_eda_sent_relation.write(str(new_line) + '\n')

    TRAIN_SENT_ID = 1
    for index in range(len(eda_sents)):
        sent_id = "TRAIN_SENT_ID_" + '%07d' % TRAIN_SENT_ID
        new_sent = eda_sents[index].strip('\n').split('\t')[1]

        index2 = int(index / 17)
        name1 = src_sents[index2].strip('\n').split('\t')[1]
        name2 = src_sents[index2].strip('\n').split('\t')[2]

        name1_id = sent_id + '_1'
        name2_id = sent_id + '_2'
        name1_pos = str([new_sent.find(name1), new_sent.find(name1) + len(name1)])
        name2_pos = str([new_sent.find(name2), new_sent.find(name2) + len(name2)])

        new_line = sent_id + '\t' + name1 + '\t' + name1_id + '\t' + name1_pos + '\t' + name2 + '\t' + name2_id + '\t' + name2_pos + '\t' + new_sent
        TRAIN_SENT_ID = TRAIN_SENT_ID + 1
        wf_eda_sent_train.write(str(new_line) + '\n')
        print(new_line)

    rf_sent.close()
    rf_relation.close()
    rf_eda_train.close()
    wf_eda_sent_train.close()
    wf_eda_sent_relation.close()
