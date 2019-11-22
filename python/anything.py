from preprocessor import preprocess
import time
from tqdm import tqdm
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


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print("%s function took %0.3f ms" %
              (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


"""
    so/nso それぞれにしかないタグを、2,3,4,5,6-グラムでそれぞれ出力
"""


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print("%s function took %0.3f ms" %
              (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


class UniquTags:

    """
    so/nso それぞれにしかないタグを、2,3,4,5,6-グラムでそれぞれ出力
    """

    def remove_tags(self, data):
        """
            一定値以下の出現頻度のタグは削除して配列を返す
        """
        print("Removing too low frequency tags")
        idx = 0
        min_value = 0.00001
        for i, elem in enumerate(data):
            if float(elem[1]) < min_value:
                idx = i
                break

        return data[0:idx]

    def data_filename(self, s_type, n):
        """
            so/nso の ngram のファイル名を返す
        """
        return '%s/%s_%sgrams.txt' % (ngrams_path, s_type, n)

    def ngram_data(self, filename):
        """
            tag と 出現頻度の値を分割した配列を要素とした配列を返す
        """
        file = open(filename).read().strip().split('\n')
        data = [elem.split(': ') for elem in file]
        return data

    @timing
    def common_tags(self, n):
        """
            so/nso 共通のタグを返す
        """
        so_ngrams_filename = data_filename('so', n)
        nso_ngrams_filename = data_filename('nso', n)
        all_tags = []
        for filename in [so_ngrams_filename, nso_ngrams_filename]:
            data = ngram_data(filename)
            [all_tags.append(elem[0]) for elem in data]
        print("Finding common tags")
        seen = {}
        commons = set()
        for tag in all_tags:
            if tag not in seen:
                seen[tag] = 1
            else:
                if seen[tag] == 1:
                    commons.add(tag)
                seen[tag] += 1
        return commons

    @timing
    def unique_tags(self, n, commons, s_type):
        """
            so/nso それぞれのみに存在するタグを返す
        """
        ngrams_filename = data_filename(s_type, n)
        data = ngram_data(ngrams_filename)
        data = remove_tags(data)
        tags = [tag[0] for tag in tqdm(data)]
        unique = []
        for tag in tqdm(tags):
            if tag not in commons:
                unique.append(tag)
        return unique

    def execute(self):
        ngrams_path = '/Users/shohei/Desktop/tsukuba/research/master/data/results/ngrams'
        for n in [2, 3, 4, 5, 6]:
            commons = common_tags(n)
            so_unique = unique_tags(n, commons, 'so')
            nso_unique = unique_tags(n, commons, 'nso')
            print('so', n, len(so_unique))
            print('nso', n, len(nso_unique))


def find_not_but_syntax():
    """
        Let's search "not ~ but syntax" !!!
    """

    so_path = (
        "/Users/shohei/Tsukuba/tsukuba/research/master/data/speech_original_transcripts/so"
    )

    for idx, filename in enumerate(glob.glob(f"{so_path}/*")):
        sentences = preprocess(filename)
        for sentence in sentences:
            if "not" in sentence:
                if "but" in sentence:
                    print()
                    print(sentence)
        if idx == 0:
            break


class UnableCheckSpeeches:

    """
    卒論時に、SO でも NSO でもなく、チェックできなかったスピーチを取得するコード
    """

    def remove_double_empty(self, lst):
        """
        連続した空白を削除
        """
        return [re.sub(r'\s+', r' ', elem) for elem in lst]

    def leave_only_chara_and_number(self, lst):
        """
            記号と数字以外を空白に変換し、要素を小文字に変換
        """
        return [re.sub(r'[^a-z0-9\s]', r'', elem.lower().strip()) for elem in lst]

    def execute(self):
        all_speeches = open(
            '../data/all_titles.txt').read().strip().split('\n')
        so_speeches = open('../data/so_titles.txt').read().strip().split('\n')
        nso_speeches = open(
            '../data/nso_titles.txt').read().strip().split('\n')

        all_speeches = remove_double_empty(
            leave_only_chara_and_number(all_speeches))
        so_speeches = remove_double_empty(
            leave_only_chara_and_number(so_speeches))
        nso_speeches = remove_double_empty(
            leave_only_chara_and_number(nso_speeches))

        for so in so_speeches:
            if so in all_speeches:
                all_speeches.remove(so)

        for nso in nso_speeches:
            if nso in all_speeches:
                all_speeches.remove(nso)

        with open('../data/unable_checked_speech_titles.txt', 'a') as f:
            for speech in all_speeches:
                f.write('%s\n' % speech)
