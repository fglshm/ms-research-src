"""
    スピーチの時間が似たスピーチを数える
    間隔は 10s とする
"""
import pandas as pd
import math
import csv
import os

duration_file_path = '/Users/shohei/Tsukuba/tsukuba/research/master/src/others/ted/duration'
speech_types = ['so', 'nso']
interval = 60

for speech_type in speech_types:
    df = pd.read_csv(
        f'{duration_file_path}/speeches/{speech_type}.csv', header=None)

    first_duration = math.floor(df[1].iloc[0] / 60) * 60
    last_duration = math.floor(df[1].iloc[-1] / 60) * 60 + 60

    print(first_duration, last_duration)
    thres = first_duration
    while thres < last_duration:
        csv_file = f'{duration_file_path}/{interval}seconds/{speech_type}/{thres}_{thres+interval}.csv'
        freq = df.loc[df[1] < thres + 60]
        freq = freq.loc[freq[1] > thres]

        print(thres, thres + interval, speech_type, len(freq))

        with open(csv_file, 'w') as f:
            writer = csv.writer(f)
            for f in freq[0]:
                writer.writerow([f])

        thres += 60
