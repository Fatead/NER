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
import http.client
import hashlib
import urllib
import random
import json
import time
from definitions import DATA_DIR


if __name__ == '__main__':
    rf_sent_path = DATA_DIR + '/test/sent_test.txt'
    rf_relation_path = DATA_DIR + '/test/sent_relation_test.txt'
    wf_bt_sent_train_path = DATA_DIR + '/test/bt_sent_test.txt'
    wf_bt_sent_relation_path = DATA_DIR + '/test/bt_sent_relation.txt'
    rf_sent = open(rf_sent_path, 'r', encoding='UTF-8')
    rf_relation = open(rf_relation_path, 'r', encoding='UTF-8')
    wf_bt_sent_train = open(wf_bt_sent_train_path, 'w', encoding='UTF-8')
    wf_bt_sent_relation = open(wf_bt_sent_relation_path, 'w', encoding='UTF-8')

    src_sents = []
    src_relations = []

    for line in rf_sent:
        src_sents.append(line)
    for line in rf_relation:
        src_relations.append(line)

    appid = '20200623000504716'  # 填写你的appid
    secretKey = 'xClk3m2VGITIgSXq8KCg'  # 填写你的密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'
    ChineseLang = 'zh'  # 原文语种，填写中文 (zh)，也可自动识别 (填auto)
    EnglishLang = 'en'  # 译文语种，填英文 (en)

    TRAIN_SENT_ID = 38418
    for index, src_relation in enumerate(src_relations):
        relation_id = src_relation.strip('\n').split('\t')[1]
        if relation_id != '0':
            name1 = src_sents[index].strip('\n').split('\t')[1]
            name2 = src_sents[index].strip('\n').split('\t')[2]
            src_sent = src_sents[index].strip('\n').split('\t')[3]
            querys = [src_sent]
            results = []
            for query in querys:
                try:
                    httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
                    # 翻译成英文，from=ChineseLang，to=EnglishLang
                    salt = random.randint(32768, 65536)
                    sign = appid + query + str(salt) + secretKey
                    sign = hashlib.md5(sign.encode()).hexdigest()
                    first_url = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(query) + '&from=' + \
                                ChineseLang + '&to=' + EnglishLang + '&salt=' + str(salt) + '&sign=' + sign
                    httpClient.request('GET', first_url)
                    response = httpClient.getresponse()
                    result_all = response.read().decode("utf-8")
                    english_result = json.loads(result_all)
                    english_result = english_result['trans_result'][0]['dst']
                    # print('翻译结果: ', english_result)
                    # 本人使用的是通用翻译 API 的标准版，请求之间要限制频率，等待一秒
                    time.sleep(1)
                    # 翻译回中文，from=EnglishLang，to=ChineseLang
                    salt = random.randint(32768, 65536)
                    sign = appid + english_result + str(salt) + secretKey
                    sign = hashlib.md5(sign.encode()).hexdigest()
                    second_url = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(english_result) + '&from=' + \
                                 EnglishLang + '&to=' + ChineseLang + '&salt=' + str(salt) + '&sign=' + sign
                    httpClient.request('GET', second_url)
                    response = httpClient.getresponse()
                    result_all = response.read().decode("utf-8")
                    chinese_result = json.loads(result_all)
                    chinese_result = chinese_result['trans_result'][0]['dst']
                    time.sleep(1)
                    # print('回译结果: ', chinese_result)
                    results.append(chinese_result)
                except Exception as e:
                    print(e)
                    results = []
                    break
            if results:
                # name1 = results[0]
                # name2 = results[1]
                sent = results[0]
                sent_id = "TRAIN_SENT_ID_" + '%06d' % TRAIN_SENT_ID
                name1_id = sent_id + '_1'
                name2_id = sent_id + '_2'
                name1_pos = str([sent.find(name1), sent.find(name1) + len(name1)])
                name2_pos = str([sent.find(name2), sent.find(name2) + len(name2)])
                sent_line = sent_id + '\t' + name1 + '\t' + name1_id + '\t' + name1_pos + '\t' + name2 + '\t' + name2_id + '\t' + name2_pos + '\t' + sent
                wf_bt_sent_train.write(str(sent_line.strip('\n')) + '\n')
                print(sent_line)
                relation_line = sent_id + '\t' + relation_id
                wf_bt_sent_relation.write(str(relation_line.strip('\n')) + '\n')
                print(relation_line)
                TRAIN_SENT_ID = TRAIN_SENT_ID + 1
# from googletrans import Translator
# from definitions import DATA_DIR
# # from py_translator import Translator
# from translate import Translator
#
#
# if __name__ == '__main__':
#     rf_path = DATA_DIR + '/train/translation_sent_train.txt'
#     wf_path = DATA_DIR + '/train/back_translation_sent_train.txt'
#     rf_name = open(rf_path, 'r', encoding='UTF-8')
#     wf_name = open(wf_path, 'w', encoding='UTF-8')
#
#     # t = Translator(service_urls=['translate.google.cn'])
#     # t = Translator(service_urls=['translate.google.cn'])
#
#     translator1 = Translator(from_lang="chinese", to_lang="english")
#     translator2 = Translator(to_lang="chinese")
#
#     for line in rf_name:
#         all_field = line.strip('\n').split('\t')
#         name1 = all_field[0]
#         name2 = all_field[1]
#         sent = all_field[2]
#
#         en_name1 = translator1.translate(name1)
#         en_name2 = translator1.translate(name2)
#         en_sent = translator1.translate(sent)
#
#         zh_name1 = translator2.translate(en_name1)
#         zh_name2 = translator2.translate(en_name2)
#         zh_sent = translator2.translate(en_sent)
#
#         new_line = zh_name1 + '\t' + zh_name2 + '\t' + zh_sent
#
#         wf_name.write(str(new_line) + '\n')
#         print(new_line)
#
#     rf_name.close()
#     wf_name.close()
