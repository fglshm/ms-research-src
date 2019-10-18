"""
    文の単語数に着目した前後の文の類似度の分析
    1. 変化の度合いが大きい文のペアはスピーチのどこで出現するか.
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


class Data:
    """
        単語数に基づく文の前後の文の類似度データを保持するクラス
    """

    def __init__(self, speech_type):
        self.similarities = self.load_similarities(speech_type)

    def load_similarities(self, speech_type):
        values = np.load(f"{speech_type}_similarities.npy")
        values = [np.array(elem) for elem in values]
        return values


class Analyzer:
    """
        1スピーチの中で, 前後の文の単語数の違いが顕著な文のペアを取得するクラス
    """

    def __init__(self, similarities):
        self.similarities = similarities
        self.prev_values = self.similarities
        self.N = self.similarities.shape[0]
        self.frequency = np.zeros(10)

    def calculate(self):
        """
            平均以上の類似度を求める
        """
        sentence = self.similarities
        while True:
            values = self.prev_values
            avg = np.average(values)
            over_avg_idx = np.where(sentence > avg)
            over_avg = sentence[over_avg_idx]
            self.prev_values = over_avg
            if len(over_avg) < self.N / 20:
                return avg, over_avg_idx[0], over_avg

    def position(self, values):
        pos = np.divide(values, self.N)
        return pos

    def get_frequency(self, lst):
        """
            度数を求めてそのリストを返す
        """
        for elem in lst:
            idx = int(elem*10)
            self.frequency[idx] += 1

    def draw(self):
        """
            分析中のスピーチの前後の文の類似度をグラフ表示する
        """
        plt.plot(self.similarities)
        plt.show()


def main():
    data = Data("nso")
    frequencies = np.zeros(10)
    sent_num = 0
    for similarity in tqdm(data.similarities):
        analyzer = Analyzer(similarity)
        sent_num += analyzer.N
        avg, idx, values = analyzer.calculate()
        position = analyzer.position(idx)
        analyzer.get_frequency(position)
        frequencies = np.add(frequencies, analyzer.frequency)
    print(frequencies)
    print(sent_num)


if __name__ == "__main__":
    main()
