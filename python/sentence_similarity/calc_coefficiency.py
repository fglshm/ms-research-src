import glob
import numpy as np
import os
import csv

pathes = glob.glob('/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/diff/60seconds/*')
dirs = [glob.glob(f'{path}/5/*') for path in pathes]
dirs = [dir for dir in dirs if len(dir) == 2]

dirs = sorted(dirs)

speech_counts = sorted(open('/Users/shohei/Tsukuba/tsukuba/research/master/src/python/60duration_speeches.csv').read().strip().split('\n'))
so_count = [elem.split(',')[1] for elem in speech_counts]
nso_count = [elem.split(',')[2] for elem in speech_counts]

sum_count = [int(so) + int(nso) for so, nso in zip(so_count, nso_count)]

corrcoef_array = []

results = []

for idx, dir in enumerate(dirs):
    time_span = dir[0].split('/')[-3]
    np_arrays = [np.load(file) for file in dir]
    corrcoef = np.round(np.corrcoef(np_arrays[0], np_arrays[1]), 4)
    corrcoef_array.append(corrcoef[0][1])

    results.append([time_span, corrcoef[0][1], so_count[idx], nso_count[idx], sum_count[idx]])
    
speech_count_corr = np.corrcoef(sum_count, corrcoef_array)
print(np.round(speech_count_corr[0][1], 3))


with open('60seconds_correlation_coefficient.csv', 'w') as f:
    writer = csv.writer(f)
    for result in results:
        writer.writerow(result)