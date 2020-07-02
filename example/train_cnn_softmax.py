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
from pathlib import Path
import torch
import numpy as np
import json
import opennre
from definitions import ROOT_DIR
from opennre import encoder, model, framework
import os
from gensim.models import KeyedVectors

ckpt_dir = Path(ROOT_DIR) /"model"/ "ner" / "ckpt"
ckpt_dir.mkdir(exist_ok=True, parents=True)
ckpt = str(ckpt_dir / "cnn_softmax.pth.tar")

rel2id = json.load(open(str(Path(ROOT_DIR) / "data" / "clean" / "src_data" / "rel2id.json")))
print(rel2id)
wordi2d = json.load(open(os.path.join(ROOT_DIR, 'pretrain/glove/glove.6B.300d_word2id.json')))
# word2vec = np.load(os.path.join(ROOT_DIR, 'pretrain/glove/glove.6B.300d_mat.npy'))
word2vec = KeyedVectors.load_word2vec_format(os.path.join(ROOT_DIR, 'pretrain/glove/glove.6B.300d_mat.npy'), binary=False)

# Define the sentence encoder
sentence_encoder = opennre.encoder.CNNEncoder(
    token2id=wordi2d,
    max_length=40,
    word_size=50,
    position_size=5,
    hidden_size=230,
    blank_padding=True,
    kernel_size=3,
    padding_size=1,
    word2vec=word2vec,
    dropout=0.5
)

model = opennre.model.SoftmaxNN(sentence_encoder, len(rel2id)+1, rel2id)
framework = opennre.framework.SentenceRE(
    train_path=str(Path(ROOT_DIR) / "data" / "clean" / "src_data" / "train_1.txt"),
    val_path=str(Path(ROOT_DIR) / "data" / "clean" / "src_data" / "val.txt"),
    test_path=str(Path(ROOT_DIR) / "data" / "clean" / "src_data" / "test.txt"),
    model=model,
    ckpt=ckpt,
    batch_size=32,
    max_epoch=10,
    lr=3e-5,
    opt='adam')
# Train
framework.train_model(metric='micro_f1')
# Test
framework.load_state_dict(torch.load(ckpt)['state_dict'])
result = framework.eval_model(framework.test_loader)
print('Accuracy on test set: {}'.format(result['acc']))
print('Micro Precision: {}'.format(result['micro_p']))
print('Micro Recall: {}'.format(result['micro_r']))
print('Micro F1: {}'.format(result['micro_f1']))
