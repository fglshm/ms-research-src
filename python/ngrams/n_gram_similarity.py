"""
    nグラムに着目した文の類似度を求める
"""

from preprocessor import preprocess
from nlp import NLP
import numpy as np
import matplotlib.pyplot as plt


def n_gram(n, sentence):
    """
        1文のnグラムの形態素のリストを抽出
    """
    nlp = NLP()
    tokens = nlp.tokens(sentence)
    tokens = nlp.rm(tokens)
    tags = nlp.tags(tokens)
    sent_2grams = nlp.ngrams(tags, 2)
    tags = []
    for elems in sent_2grams:
        lst = []
        for elem in elems:
            lst.append(elem[1])
        tags.append("|".join(lst))
    return tags


def common_n_grams(gram1, gram2):
    """
        gram1 と gram2 の共通要素をリストで返す
    """
    sum_gram = gram1 + gram2
    common = [elem for elem in sum_gram if sum_gram.count(elem) > 1]
    return unique(common)


def n_gram_list(gram1, gram2):
    """
        sentence1 と sentence2 で出現する n-gram のパターン
    """
    sum_gram = gram1 + gram2
    seen = set()
    for gram in sum_gram:
        if gram not in seen:
            seen.add(gram)
    return seen


def unique(lst):
    """
        lst の重複要素を削除した結果を返す
    """
    return list(set(lst))


def sentence_tags(sentence):
    """
        1文の形態素をリストで返す
    """
    nlp = NLP()
    tokens = nlp.rm(nlp.tokens(sentence))
    tags = nlp.tags(tokens)
    tags = [elem[1] for elem in tags]
    return tags


speech_type = "nso"
speech_id = "2206"

path = "/Users/shohei/Tsukuba/tsukuba/research/master/data/speech_original_transcripts"
filename = f"{path}/{speech_type}/{speech_id}.txt"
sentences = preprocess(filename)

similarities = []

for idx in range(len(sentences) - 1):
    sent1 = sentences[idx]
    sent1_2gram = n_gram(2, sent1)
    sent1_2gram = unique(sent1_2gram)

    sent2 = sentences[idx + 1]
    sent2_2gram = n_gram(2, sent2)
    sent2_2gram = unique(sent2_2gram)

    common = common_n_grams(sent1_2gram, sent2_2gram)

    all_n_grams = n_gram_list(sent1_2gram, sent2_2gram)

    similarity = round(len(common) / len(all_n_grams), 3)
    similarities.append(similarity)


similarities = np.array(similarities)
color = "blue" if speech_type == "so" else "red"
axes = plt.axes()
axes.set_ylim([0, 1])
plt.plot(similarities, color=color)
plt.title("similarity based on 2-gram")
plt.xlabel("sentence")
plt.ylabel("similarity")
figure = plt.gcf()
figure.set_size_inches(20, 10)
plt.show()
