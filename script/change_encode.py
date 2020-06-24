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
from chardet import detect

from definitions import DATA_DIR

if __name__ == '__main__':
    fn = DATA_DIR + '/wiki_cn'
    with open(fn, 'rb') as f:
        s = f.read()

    newf = DATA_DIR + '/wiki_cn_new.txt'
    with open(newf, 'wb') as f:
        f.write(s.decode('ignore').encode('utf8'))
    print('done!convert coding to utf-8 and wirte content in `{}`'.format(newf))
