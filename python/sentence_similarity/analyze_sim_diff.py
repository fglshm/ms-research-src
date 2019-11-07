"""
    スピーチ時間が似ている SO/NSO スピーチの, 文の類似度の変化が最大値の位置を比較
"""

import glob
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from tqdm import tqdm

if len(sys.argv) != 2:
    print("Please enter time span (ex. 10, 60)")
    sys.exit()

interval = sys.argv[1]
figure_save_path = f'/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/diff/figure/{interval}seconds/5'
time_spans_path = f'/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/diff/{interval}seconds'
time_spans_dirs = glob.glob(f'{time_spans_path}/*')
time_spans = sorted([os.path.basename(dir) for dir in time_spans_dirs])

for idx, time_span in tqdm(enumerate(time_spans)):
    files = glob.glob(
        f'/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/diff/{interval}seconds/{time_span}/5/*')

    if len(files) == 2:
        peaks = [np.load(filename) for filename in sorted(files)]

        w = 0.4

        Y1 = peaks[0]
        Y2 = peaks[1]

        X = np.arange(len(Y1))  # [0, 1, 2]

        # nso
        plt.bar(X, Y1, color='skyblue', width=w, label='NSO', align="center")

        # so
        plt.bar(X + w, Y2, color='tomato', width=w, label='SO', align="center")

        # 凡例を表示
        plt.legend(loc="best")
        plt.title(f'{time_span}s')

        figure = plt.gcf()
        figure.set_size_inches(20, 10)

        plt.savefig(f"{figure_save_path}/{time_span}.pdf", format="pdf")
        plt.clf()

    else:
        print("Found only one file. (so or nso).")
