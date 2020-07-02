#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: zhaocy
@Email: 19110240027@fudan.edu.cn
@Created: 2020/7/1
------------------------------------------
@Modify: 2020/7/1
------------------------------------------
@Description: 
"""
import json
from definitions import ROOT_DIR
import os

if __name__ == '__main__':
    word2id = {}
    id = 0
    with open("D:\\BaiduNetdiskDownload\\sgns.wiki.word\\sgns.wiki.word", 'r', encoding='UTF-8') as rf:
        with open(os.path.join(ROOT_DIR, 'pretrain\\glove\\glove.6B.300d_word2id.json'), 'w', encoding='UTF-8') as wf:
            for index, line in enumerate(rf):
                if index == 0:
                    continue
                word = line.split(' ')[0]
                word2id[word] = id
                id = id + 1
            json_str = json.dumps(word2id, indent=4, ensure_ascii=False)
            wf.write(json_str)
    rf.close()
    wf.close()




