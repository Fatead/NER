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
import random

from definitions import DATA_DIR


def same_relation(src_sents, src_relations):
    wf_sree_sent_train_path = DATA_DIR + '/dev/sree_sent_dev.txt'
    wf_sree_sent_relation_path = DATA_DIR + '/dev/sree_sent_relation.txt'
    wf_sree_sent_train = open(wf_sree_sent_train_path, 'w', encoding='UTF-8')
    wf_sree_sent_relation = open(wf_sree_sent_relation_path, 'w', encoding='UTF-8')

    relation_sent = {}
    for index, src_relation in enumerate(src_relations):
        relation_id = src_relation.strip('\n').split('\t')[1]
        if relation_id != '0':
            if relation_id not in relation_sent.keys():
                relation_sent.setdefault(relation_id, [])
            relation_sent[relation_id].append(src_sents[index])

    TRAIN_SENT_ID = 38418
    for key in relation_sent:
        sents = relation_sent[key]
        for sent_index, sent in enumerate(sents):
            name1 = sent.strip('\n').split('\t')[1]
            name2 = sent.strip('\n').split('\t')[2]

            change_sents = []
            if len(sents) < 5:
                change_sents = sents
            else:
                indexes = []
                while len(indexes) < 4:
                    index = random.randrange(0, len(sents))
                    if index not in indexes and index != sent_index:
                        indexes.append(index)
                        change_sents.append(sents[index])
            for tmp_sent in change_sents:
                tmp_name1 = tmp_sent.strip('\n').split('\t')[1]
                tmp_name2 = tmp_sent.strip('\n').split('\t')[2]
                if name1 == tmp_name1 and name2 == tmp_name2:
                    continue
                else:
                    sent_id = "TRAIN_SENT_ID_" + '%06d' % TRAIN_SENT_ID
                    new_sent = tmp_sent.strip('\n').split('\t')[3].replace(tmp_name1, name1).replace(tmp_name2, name2)
                    name1_id = sent_id + '_1'
                    name2_id = sent_id + '_2'
                    name1_pos = str([new_sent.find(name1), new_sent.find(name1) + len(name1)])
                    name2_pos = str([new_sent.find(name2), new_sent.find(name2) + len(name2)])
                    sent_line = sent_id + '\t' + name1 + '\t' + name1_id + '\t' + name1_pos + '\t' + name2 + '\t' + name2_id + '\t' + name2_pos + '\t' + new_sent
                    wf_sree_sent_train.write(str(sent_line.strip('\n')) + '\n')
                    print(sent_line)
                    relation_line = sent_id + '\t' + key
                    wf_sree_sent_relation.write(str(relation_line.strip('\n')) + '\n')
                    print(relation_line)
                    TRAIN_SENT_ID = TRAIN_SENT_ID + 1


def symmetrical_relation(src_sents, src_relations):
    wf_symree_sent_train_path = DATA_DIR + '/dev/symree_sent_dev.txt'
    wf_symree_sent_relation_path = DATA_DIR + '/dev/symree_sent_relation.txt'
    wf_symree_sent_train = open(wf_symree_sent_train_path, 'w', encoding='UTF-8')
    wf_symree_sent_relation = open(wf_symree_sent_relation_path, 'w', encoding='UTF-8')

    relation_sent = {}
    for index, src_relation in enumerate(src_relations):
        relation_id = src_relation.strip('\n').split('\t')[1]
        if relation_id == '30' or relation_id == '32':
            if relation_id not in relation_sent.keys():
                relation_sent.setdefault(relation_id, [])
            relation_sent[relation_id].append(src_sents[index])

    TRAIN_SENT_ID = 38418
    for key in relation_sent:
        sents = relation_sent[key]
        for sent in sents:
            name1 = sent.strip('\n').split('\t')[1]
            name2 = sent.strip('\n').split('\t')[2]

            sent_id = "TRAIN_SENT_ID_" + '%06d' % TRAIN_SENT_ID
            new_sent = sent.strip('\n').split('\t')[3].replace(name1, "name1").replace(name2, "name2").replace("name1", name2).replace("name2", name1)
            name1_id = sent_id + '_1'
            name2_id = sent_id + '_2'
            name1_pos = str([new_sent.find(name2), new_sent.find(name1) + len(name2)])
            name2_pos = str([new_sent.find(name1), new_sent.find(name2) + len(name1)])
            sent_line = sent_id + '\t' + name2 + '\t' + name1_id + '\t' + name1_pos + '\t' + name1 + '\t' + name2_id + '\t' + name2_pos + '\t' + new_sent
            wf_symree_sent_train.write(str(sent_line.strip('\n')) + '\n')
            print(sent_line)
            relation_line = sent_id + '\t' + key
            wf_symree_sent_relation.write(str(relation_line.strip('\n')) + '\n')
            print(relation_line)
            TRAIN_SENT_ID = TRAIN_SENT_ID + 1


if __name__ == '__main__':
    rf_sent_path = DATA_DIR + '/dev/sent_dev.txt'
    rf_relation_path = DATA_DIR + '/dev/sent_relation_dev.txt'
    rf_sent = open(rf_sent_path, 'r', encoding='UTF-8')
    rf_relation = open(rf_relation_path, 'r', encoding='UTF-8')

    src_sents = []
    src_relations = []

    for line in rf_sent:
        src_sents.append(line)
    for line in rf_relation:
        src_relations.append(line)

    same_relation(src_sents, src_relations)
    symmetrical_relation(src_sents, src_relations)
