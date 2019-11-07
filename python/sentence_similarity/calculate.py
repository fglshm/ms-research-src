"""
    スピーチの時間が近いスピーチの, 文の類似度を求める
    時間の間隔は n 秒
"""

import glob
import os
import itertools
import pandas as pd
import numpy as np
from tqdm import tqdm


class Analyzer:
    def __init__(self, sim, thres):
        self.sim = sim  # 類似度のデータ
        self.prev_values = sim  # 平均を計算するときに使う, 1つ前の類似度
        self.peaks = []  # 変化の大きい文の位置 (0.00 ~ 1.00)
        self.N = sim.shape[0]  # 文の数
        self.frequency = np.zeros(100)
        self.threshold = thres

    def calculate(self):
        """
            平均以上の類似度を求める
        """
        sentence_sims = self.sim
        while True:
            values = self.prev_values
            avg = np.average(values)
            over_avg_idx = np.where(sentence_sims > avg)
            over_avg = sentence_sims[over_avg_idx]
            self.prev_values = over_avg
            if len(over_avg) < self.threshold:
                return self.get_index(np.divide(over_avg_idx[0], self.N))

    def max_position(self):
        max_idx = np.argmax(self.sim)
        max_pos = max_idx / self.N
        idx = int(np.round(max_pos, 2) * 100)
        self.frequency[idx] += 1

    def get_top_n(self, n):
        top_n_index = []
        while True:
            idx = self.sim.argmax()
            top_n_index.append(idx)
            self.sim[idx] = 0
            if len(top_n_index) == 5:
                top_n_index = np.array(top_n_index)
                top_n_position = np.divide(top_n_index, self.N)
                top_n_position = np.multiply(top_n_position, 100)
                top_n_position = np.floor(top_n_position)
                return top_n_position.astype(int)

    def get_index(self, values):
        values = np.multiply(values, 100)
        values = np.floor(values).astype(int)
        return values


time_span = 60
duration_path = '/Users/shohei/Tsukuba/tsukuba/research/master/src/others/ted/duration'
intervals = []
speech_types = ['nso', 'so']
for speech_type in speech_types:
    durations = [os.path.basename(filename).replace(
        '.csv', '') for filename in glob.glob(f'{duration_path}/{time_span}seconds/{speech_type}/*')]
    intervals.append(durations)

intervals = list(itertools.chain.from_iterable(intervals))
intervals = sorted(list(set(intervals)))

results = {}

for speech_type in speech_types:
    for interval in tqdm(intervals):

        save_path = f'/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/diff/60seconds/{interval}/5'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print("created directories")

        speech_id_file = f'/Users/shohei/Tsukuba/tsukuba/research/master/src/others/ted/duration/{time_span}seconds/{speech_type}/{interval}.csv'

        if not os.path.exists(speech_id_file) or os.stat(speech_id_file).st_size == 0:
            continue

        df = pd.read_csv(speech_id_file, header=None)

        frequencies = np.zeros(100)

        for id in df[0]:
            sim_path = f'/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/{speech_type}/{id}.npy'
            sim = np.load(sim_path)
            analyzer = Analyzer(sim, 5)
            peak_index = analyzer.get_top_n(5)
            # peak_index = analyzer.calculate()
            for idx in peak_index:
                frequencies[idx] += 1

        # analyzer.max_position()
        # frequencies = np.add(frequencies, analyzer.frequency)
        frequencies = np.divide(frequencies, len(df[0]))

        if interval in results:
            results[interval].append(np.sum(frequencies))
        else:
            results[interval] = [np.sum(frequencies)]

        # np.save(
        #     f'/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/diff/{time_span}seconds/{interval}/5/{speech_type}.npy', frequencies)

print(results)
