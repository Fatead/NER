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

if __name__ == '__main__':
    rf_path = DATA_DIR + '/dev/sent_dev.txt'
    wf_path = DATA_DIR + '/dev/sent_dev_new.txt'
    rf_name = open(rf_path, 'r', encoding='UTF-8')
    wf_name = open(wf_path, 'w', encoding='UTF-8')
    for line in rf_name:
        all_field = line.strip('\n').split('\t')
        sent_id = all_field[0]
        name1 = all_field[1]
        name2 = all_field[2]
        sent = all_field[3]

        name1_id = sent_id + '_1'
        name2_id = sent_id + '_2'
        name1_pos = str([sent.find(name1), sent.find(name1) + len(name1)])
        name2_pos = str([sent.find(name2), sent.find(name2) + len(name2)])

        new_line = sent_id + '\t' + name1 + '\t' + name1_id + '\t' + name1_pos + '\t' + name2 + '\t' + name2_id + '\t' + name2_pos + '\t' + sent

        wf_name.write(str(new_line) + '\n')
        print(new_line)

    rf_name.close()
    wf_name.close()
