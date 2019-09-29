"""
    so/nso それぞれにしかないタグを、2,3,4,5,6-グラムでそれぞれ出力
"""
from tqdm import tqdm
import re
import time


def remove_tags(data):
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


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print("%s function took %0.3f ms" %
              (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


def data_filename(s_type, n):
    """
        so/nso の ngram のファイル名を返す
    """
    return '%s/%s_%sgrams.txt' % (ngrams_path, s_type, n)


def ngram_data(filename):
    """
        tag と 出現頻度の値を分割した配列を要素とした配列を返す
    """
    file = open(filename).read().strip().split('\n')
    data = [elem.split(': ') for elem in file]
    return data


@timing
def common_tags(n):
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
def unique_tags(n, commons, s_type):
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


ngrams_path = '/Users/shohei/Desktop/tsukuba/research/master/data/results/ngrams'
for n in [2, 3, 4, 5, 6]:
    commons = common_tags(n)
    so_unique = unique_tags(n, commons, 'so')
    nso_unique = unique_tags(n, commons, 'nso')
    print('so', n, len(so_unique))
    print('nso', n, len(nso_unique))
