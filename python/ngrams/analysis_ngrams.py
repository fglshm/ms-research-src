"""
    so/nso の ngram 出力結果を分析するコード
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import sys
import itertools
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')


def get_tags(filename):
    top = get_top(filename, 100)
    tags = [elem[0] for elem in top]
    return tags


def get_top(filename, count):
    file = open(filename).read().strip().split('\n')
    top = [elem.split(': ') for elem in file[0:count]]
    return top


def get_all(filename):
    file = open(filename).read().strip().split('\n')
    data = [elem.split(': ') for elem in file]
    return data


def get_values(data):
    values = []
    for tag in unique_tags:
        for elem in data:
            if tag == elem[0]:
                values.append(elem)
    return values


ngram_file_path = '/Users/shohei/Desktop/tsukuba/research/master/data/results/ngrams'

nums = [2, 3, 4, 5, 6]
for n in nums:

    save_path = '/Users/shohei/Desktop/tsukuba/research/master/data/results/analysis/%sgrams' % str(
        n)

    so_filename = ngram_file_path + '/so_' + str(n) + 'grams.txt'
    nso_filename = ngram_file_path + '/nso_' + str(n) + 'grams.txt'

    so_tags = get_tags(so_filename)
    nso_tags = get_tags(nso_filename)
    sum_tags = so_tags + nso_tags

    # so/nso それぞれ上位 n 個のタグ
    unique_tags = list(set(sum_tags))

    # so/nso 共通のタグ
    commons = [tag for tag in set(sum_tags) if sum_tags.count(tag) > 1]

    # so だけにあるタグ
    only_so_tags = [tag for tag in set(
        so_tags + commons) if (so_tags + commons).count(tag) == 1]

    # nso だけにあるタグ
    only_nso_tags = [tag for tag in set(
        nso_tags + commons) if (nso_tags + commons).count(tag) == 1]

    # # top n のタグと出現頻度の値のペア
    so_data = get_all(so_filename)
    nso_data = get_all(nso_filename)

    so_values = get_values(so_data)
    nso_values = get_values(nso_data)

    size = 10
    splitted_tags = [unique_tags[x: x + size]
                     for x in range(0, len(unique_tags), size)]
    splitted_so_values = [so_values[x: x + size]
                          for x in range(0, len(so_values), size)]
    splitted_nso_values = [nso_values[x: x + size]
                           for x in range(0, len(nso_values), size)]

    for idx, (labels, so, nso) in tqdm(enumerate(zip(splitted_tags, splitted_so_values, splitted_nso_values))):
        plt.style.use('ggplot')
        n = len(labels)
        so_value = [float(value[1]) for value in so]
        nso_value = [float(value[1]) for value in nso]
        fig, ax = plt.subplots()
        index = np.arange(n)
        bar_width = 0.35
        opacity = 0.9
        ax.bar(index, so_value, bar_width,
               alpha=opacity, color='r', label='so')
        ax.bar(index+bar_width, nso_value, bar_width,
               alpha=opacity, color='b', label='nso')
        ax.set_xlabel('tag')
        ax.set_ylabel('frequency')
        ax.set_title('so / nso')
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels((['\n'.join(eval(t)) for t in labels]))
        ax.legend()
        figure = plt.gcf()
        figure.set_size_inches(8, 10)
        plt.savefig('%s/%s.eps' % (save_path, idx), format='eps')
