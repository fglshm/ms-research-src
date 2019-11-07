"""
    n 分台の so/nso のスピーチに対して, それぞれのスピーチの, 前後の文の単語数の違いを文の非類似度としたときに, 非類似度の上位 5 つがスピーチのどの区間で出現するかを求めた結果から, それぞれの区間で so/nso のどちらが大きいかを求める
"""
import matplotlib.pyplot as plt
import numpy as np
import glob

time_span_pathes = glob.glob(
    '/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/diff/60seconds/*')

for time_span_path in time_span_pathes:
    children = glob.glob(f'{time_span_path}/5/*')
    if len(children) == 2:
        children = sorted(children)
        nso_arr, so_arr = [np.load(file) for file in children]
        comp = so_arr == nso_arr
        same_index = np.where(comp == True)
        so_index = np.where((so_arr > nso_arr) == True)
        nso_index = np.where((so_arr < nso_arr) == True)

        # same value: -1
        # so > nso: 1
        # nso > so: 0

        result = np.zeros(100)
        result[same_index] = -1
        result[so_index] = 1
        result[nso_index] = 0

        print(time_span_path)
        print(result)
