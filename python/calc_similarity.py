"""
    分散, 標準偏差を計算
"""

import numpy as np
import sys
from statistics import mean, variance, stdev


speech_type = sys.argv[1]

# 単語数に着目した類似度の結果を読み込む
results = np.load(f"{speech_type}_similarities.npy")
stds = []
for array in results:
    vr = variance(array)
    sd = stdev(array)
    stds.append(sd)

print(round(variance(stds), 3))
