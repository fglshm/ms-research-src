"""
    TED のスピーチを形態素解析するコード
    n-gram の結果を出力
"""

from nlp import NLP
import re
import glob
from tqdm import tqdm
import itertools


def remove_words(text):
    """
        カッコに含まれている文字 (Laughter や Applause など) を削除する関数
    """
    text = re.sub(r'\([\s\w]+\)', r'', text)  # ()と()の中の文字を削除
    text = re.sub(r'[A-Z]{2}:', ' ', text)  # [A-Z][A-Z]: は発言者の名前であるため削除
    text = re.sub(r'\s+', r' ', text)  # 連続した空白を空白に変換
    return text.strip()  # 先頭と末尾の空白を削除して返す


def to_dict(lst):
    """
        key: (tag, tag)、value: count の辞書を返す関数        
    """
    dct = {}
    for tpl in lst:
        if tpl not in dct.keys():
            dct[tpl] = 1
        else:
            dct[tpl] += 1
    return dct


def tag_list(ngrams):
    """
        タグのセットのリストを返す  
    """
    lst = []
    for gram in ngrams:
        tag = [tpl[1] for tpl in gram]
        lst.append(tuple(tag))
    return lst


def run(files, speech_type, n):
    word_tags = []
    for file in tqdm(files):
        transcript = open(file).read().strip()
        transcript = remove_words(transcript)
        words = nlp.tokens(transcript)
        words = nlp.rm(words)
        tagged = nlp.tags(words)
        grams = nlp.ngrams(tagged, n)
        grams = [g for g in grams]
        word_tags.append(grams)

    word_tags = list(itertools.chain.from_iterable(word_tags))
    print(n, len(word_tags))
    count = len(word_tags)
    tags = tag_list(word_tags)
    tag_dict = to_dict(tags)
    tag_dict = sorted(tag_dict.items(), key=lambda x: -x[1])

    # result_path = '/Users/shohei/Desktop/tsukuba/research/master/data/results'

    # file = open("%s/%s_%sgrams.txt" % (result_path, speech_type, n), 'a')
    # for tag in tag_dict:
    #     file.write("%s: %s" % (tag[0], tag[1] / count))
    #     file.write('\n')


so_transcript_path = '/Users/shohei/Desktop/tsukuba/research/master/data/speech_original_transcripts/so'
nso_transcript_path = '/Users/shohei/Desktop/tsukuba/research/master/data/speech_original_transcripts/nso'

nlp = NLP()

so_files = glob.glob("%s/*" % so_transcript_path)
nso_files = glob.glob("%s/*" % nso_transcript_path)

for i in range(5):
    run(so_files, 'so', i+2)
    run(nso_files, 'nso', i+2)
