"""
    ngrams の結果を、出現頻度の差が大きい順にソートする (so/nso それぞれを基準にした結果を出力)
    header (so/nso based): tag set, n times, so/nso frequency, nso/so frequency
"""

import sys
from tqdm import tqdm
from operator import itemgetter


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


def remove_tags(data):
    """
        一定値以下の出現頻度のタグは削除して配列を返す
    """
    print("Removing too low frequency tags")
    idx = 0
    min_value = 0.0001
    for i, elem in enumerate(data):
        if float(elem[1]) < min_value:
            idx = i
            break

    return data[0:idx]


def common_tags(n):
    """
        so/nso 共通のタグを返す
    """
    so_ngrams_filename = data_filename('so', n)
    nso_ngrams_filename = data_filename('nso', n)
    common_tags = []
    for filename in [so_ngrams_filename, nso_ngrams_filename]:
        data = ngram_data(filename)
        data = remove_tags(data)
        [common_tags.append(elem[0]) for elem in data]
    print("Finding common tags")
    common_tags = [tag for tag in tqdm(set(
        common_tags)) if common_tags.count(tag) == 2]
    return common_tags


def common_tag_frequencies(lst, n):
    """
        共通タグの出現頻度を算出して、要素が[tag, so_frequency, nso_frequency] の配列を返す
    """
    print("Calculating frequencies of common tag")
    common_tag_frequencies = []
    so_data = ngram_data(data_filename('so', n))
    nso_data = ngram_data(data_filename('nso', n))
    so_tags, so_values = [elem[0]
                          for elem in so_data], [elem[1] for elem in so_data]
    nso_tags, nso_values = [elem[0]
                            for elem in nso_data], [elem[1] for elem in nso_data]
    for tag in tqdm(lst):
        so_idx = so_tags.index(tag)
        nso_idx = nso_tags.index(tag)
        so_value = so_values[so_idx]
        nso_value = nso_values[nso_idx]
        common_tag_frequencies.append([tag, so_value, nso_value])

    return common_tag_frequencies


def frequency_gaps(lst, s_type):
    """
        so/nso の 共通タグの frequency の商 (=n_times) を計算し、要素: [tag, n_time, so_f, nso_f] を要素とした配列を返す
        s_type (so/nso) によって、商の計算の分母を変える
    """
    print("Calculating how many times the so tag's frequency larger than that of nso")
    frequency_gaps_set = []
    focus_idx = 1 if s_type == 'so' else 2
    unfocus_idx = 2 if s_type == 'so' else 1
    for elem in tqdm(lst):
        tag = ':'.join(eval(elem[0]))
        focus_value = float(elem[focus_idx])
        unfocus_value = float(elem[unfocus_idx])
        n_times = focus_value / unfocus_value
        frequency_gaps_set.append(
            [tag, str(n_times), str(focus_value), str(unfocus_value)])

    return frequency_gaps_set


def sort_by_index(idx, lst):
    lst.sort(key=itemgetter(idx))
    lst.reverse()
    return lst


def save_results(n, data):
    """
        結果を保存
    """
    print("Saving the results")
    save_path = '/Users/shohei/Desktop/tsukuba/research/master/data/results/ngrams_gaps/over0_0001'
    save_filename = '%s/%sgrams.txt' % (save_path, n)
    f = open(save_filename, 'a')
    for elem in data:
        f.write("%s\n" % ",".join(elem))


ngrams_path = '/Users/shohei/Desktop/tsukuba/research/master/data/results/ngrams'
for n in [2, 3, 4, 5, 6]:
    print("Executing %d-gram" % n)
    tags = common_tags(n)
    frequencies = common_tag_frequencies(tags, n)
    gaps = frequency_gaps(frequencies, 'so')
    sorted_gaps = sort_by_index(1, gaps)
    save_results(n, sorted_gaps)
