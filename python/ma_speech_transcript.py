"""
    TED のスピーチを形態素解析するコード
    n-gram の結果を出力
"""

from nlp import NLP
import re


def remove_words(text):
    """
        カッコに含まれている文字 (Laughter や Applause など) を削除する関数
    """
    text = re.sub(r'\(.+\)', r'', text)
    text = re.sub(r'\s+', r' ', text)
    return text


def to_dict(lst):
    """
        key: (tag, tag)、value: count の辞書を返す関数        
    """
    dict = {}
    for tpl in lst:
        if tpl not in dict.keys():
            dict[tpl] = 1
        else:
            dict[tpl] += 1
    return dict


nlp = NLP()

# ここで TED のテキストを代入する
sentence = "Natural Language Processing with Python provides a practical introduction to programming for language processing. Written by the creators of NLTK, it guides the reader through the fundamentals of writing Python programs, working with corpora, categorizing text, analyzing linguistic structure, and more. The online version of the book has been been updated for Python 3 and NLTK 3."
sentence = remove_words(sentence)
words = nlp.tokens(sentence)
words = nlp.rm(words)
tagged = nlp.tags(words)
grams = nlp.ngrams(tagged, 2)
tags = []
word_set = []
for g in grams:
    first_word = g[0][0]
    second_word = g[1][0]
    first_tag = g[0][1]
    second_tag = g[1][1]
    word = [first_word, second_word]
    tag = (first_tag, second_tag)
    word_set.append(word)
    tags.append(tag)
    print(word, tag)

tag_dict = to_dict(tags)
tag_dict = sorted(tag_dict.items(), key=lambda x: -x[1])
print(tag_dict)
print()
print(word_set)
