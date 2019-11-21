"""
    一文の単語数に着目した文の類似度の分析
    1. 非類似度が高い文の組みの出現位置
"""

import sys
import numpy as np


speech_type = sys.argv[1]
similarities = np.load(f"{speech_type}_similarities.npy")
similarities = [np.array(arr) for arr in similarities]

means = [np.mean(arr) for arr in similarities]
# 1回目の平均以上の値の配列
# v1_arr = [x[np.where(x > mean)] for x, mean in enumerate(similarities, means)]

print(similarities[0])
print(means[0])

# for mean, x in enumerate(similarities, means):
#     print(mean, x)
