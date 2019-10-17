"""
    文の類似度を求める
    1. 単語数
    2. n-grams
    3. 疑問文か平叙文
    4. 形態素の出現頻度
    5. 形態素の並び
    6. 係り受け関係
"""

from preprocessor import preprocess
from nlp import NLP
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from tqdm import tqdm


def word_count_similarity(path, speech_type, speech_id):
    """
        1文同士の類似度を, 1文の単語数に着目して計算する
        non-similarity = t番目の文の単語数 / (t-1)番目の文の単語数
        non-similarityをsin波のように出力する
        non-similarityの値が大きいほど類似度は低い
    """
    file_path = f"{path}/{speech_type}/{speech_id}.txt"
    sentences = preprocess(file_path)
    nlp = NLP()
    tokens_list = [nlp.rm(nlp.tokens(s)) for s in sentences]
    word_counts = [len(token) for token in tokens_list]
    if 0 in word_counts:
        word_counts.remove(0)
    similarities = [0.0]
    for idx in range(len(word_counts) - 1):
        if int(word_counts[idx]) != 0:
            sim = round(int(word_counts[idx]) / int(word_counts[idx - 1]), 2)
            similarities.append(sim)

    return similarities


def save_plt(similarities, speech_type, speech_id):
    x = np.array(similarities)
    y = np.arange(x.shape[0])
    color = "blue" if speech_type == "so" else "red"
    plt.title(f"speech {speech_id} sentence non-similarity about word count")
    plt.xlabel("sentence")
    plt.ylabel("non-similarity")
    plt.plot(y, x, color=color)
    save_path = "/Users/shohei/Documents/Tsukuba/Research/results/similarity/word_count"
    figure = plt.gcf()
    figure.set_size_inches(20, 10)
    plt.savefig(
        f"{save_path}/{speech_type}/{speech_type}_{speech_id}.pdf", format="pdf"
    )
    similarities = []
    plt.clf()


speech_types = ["so", "nso"]
path = "/Users/shohei/Tsukuba/tsukuba/research/master/data/speech_original_transcripts"
for speech_type in speech_types:
    all_similaritites = []
    files = glob.glob(f"{path}/{speech_type}/*")
    for file in tqdm(files):
        speech_id = os.path.basename(file).split(".")[0]
        all_similaritites.append(word_count_similarity(path, speech_type, speech_id))
    np_sim = np.array(all_similaritites)
    np.save(f"{speech_type}_similarities.npy", np_sim)
