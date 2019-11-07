"""
    SO/NSO スピーチの文の類似度を npy ファイルで保存する
"""

import sys
sys.path.append('..')
import similarity
import numpy as np
import glob
from tqdm import tqdm

transcript_path = '/Users/shohei/Tsukuba/tsukuba/research/master/dataset/transcript'
id_files = sorted(glob.glob('/Users/shohei/Tsukuba/tsukuba/research/master/dataset/id/*'))
speech_ids = [open(filename).read().strip().split('\n') for filename in id_files]
speech_types = ['nso', 'so']
for speech_id, speech_type in tqdm(zip(speech_ids, speech_types)):
    for id in speech_id:
        sim = similarity.word_count_similarity(transcript_path, speech_type, id)
        sim = np.array(sim)
        np.save(f"/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/{speech_type}/{id}.npy", sim)