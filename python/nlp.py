#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    自然言語処理関連の関数をまとめたクラス: NLP
"""

import nltk
import re


class NLP:
    def tokens(self, text):
        """
            text の token を取得する関数
        """
        return nltk.word_tokenize(text)

    def ngrams(self, lst, n):
        """
            n_gram を出力する関数
        """
        return nltk.ngrams(lst, n)

    def rm(self, lst):
        """
            単語が要素のリストから、不要な文字を削除する関数
        """
        pattern = re.compile(r"\w")
        for i, word in enumerate(lst):
            if not pattern.findall(word):
                del lst[i]
        return lst

    def tags(self, lst):
        """
            単語のタグ付け (品詞) をする関数
        """
        tagged = nltk.pos_tag(lst)
        return tagged
