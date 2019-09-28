#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nlp import NLP
import re


def remove_words(text):
    """
        カッコに含まれている文字 (Laughter や Applause など) を削除する関数
    """
    text = re.sub(r'\(.+\)', r'', text)  # ()と()の中の文字を削除
    text = re.sub(r'[A-Z]{2}:', ' ', text)  # [A-Z][A-Z]: は発言者の名前であるため削除
    text = re.sub(r'\s+', r' ', text)  # 連続した空白を空白に変換
    return text.strip()  # 先頭と末尾の空白を削除して返す


nlp = NLP()
sentence = "you'll see it probably spinning this direction. Now I want you to keep looking at it. Move your eyes around, blink, maybe close one eye. And suddenly it will flip, and start spinning the opposite direction. Yes? Raise your hand if you got that. Yes? Keep blinking ... (Continuous sound) (Sound changes momentarily) (Sound changes momentarily) (Sound changes momentarily) (Sound changes momentarily) (Sound changes momentarily) Beau Lotto: He finds it. Amazing, right? So not only can we create a prosthetic for the visually impaired"
sentence = remove_words(sentence)
tokens = nlp.tokens(sentence)
tokens = nlp.rm(tokens)
tags = nlp.tags(tokens)
print(tags)
