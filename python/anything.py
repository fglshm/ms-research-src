import glob
import re
import os
import csv
import math
import pandas as pd
import sys


def calculate_speech_total_duration(speech_type):
    """
        so もしくは nso のスピーチの総時間を求める
        Parameters
        ----------
        speech_type : string
    """
    file_path = f'/Users/shohei/Tsukuba/research/master/src/others/ted/duration/speeches/{speech_type}.csv'
    file = open(file_path).read().strip().split('\n')
    sum_duration = 0

    for elem in file:
        sum_duration += int(elem.split(',')[1])

    print(sum_duration)


def count_similart_duration_speech_count():
    """
        スピーチの時間が似たスピーチを数える
        間隔は 60s とする
    """

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


def count_60_duration_speeches():
    path = '/Users/shohei/Tsukuba/tsukuba/research/master/src/others/ted/duration/60seconds'

    so_dirs = glob.glob(f'{path}/so/*')
    so_time_span_pathes = sorted(
        list(map(lambda x: os.path.basename(x), so_dirs)))

    nso_dirs = glob.glob(f'{path}/nso/*')
    nso_time_span_pathes = sorted(
        list(map(lambda x: os.path.basename(x), nso_dirs)))

    sum_time_span_pathes = so_time_span_pathes + nso_time_span_pathes
    time_span_pathes = sorted(
        [x for x in set(sum_time_span_pathes) if sum_time_span_pathes.count(x) > 1])

    so_speech_count = list(map(lambda x: len(
        open(f'{path}/so/{x}').read().strip().split()), time_span_pathes))
    nso_speech_count = list(map(lambda x: len(
        open(f'{path}/nso/{x}').read().strip().split()), time_span_pathes))

    print(nso_speech_count)

    with open('60duration_speeches.csv', 'w') as f:
        writer = csv.writer(f)
        [print(re.sub(r'\.csv', r'', span), so, nso) for span, so,
         nso in zip(time_span_pathes, so_speech_count, nso_speech_count)]
        for span, so, nso in zip(time_span_pathes, so_speech_count, nso_speech_count):
            writer.writerow([re.sub(r'\.csv', r'', span), so, nso])
