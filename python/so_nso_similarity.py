"""
    Calculate the number of words in a sentence,
    and display the graph that the y-axis is the number of words,
    and x-axis is sentence number
"""

import re
import nltk
from nlp import NLP
from statistics import mean, median, variance, stdev
import pandas as pd
from tqdm import tqdm
import glob
import os
from preprocessor import preprocess

nlp = NLP()

base_path = (
    "/Users/shohei/Tsukuba/tsukuba/research/master/data/speech_original_transcripts"
)
speech_types = ["nso", "so"]
for standing_ovation, speech_type in enumerate(speech_types):
    df = pd.DataFrame(
        columns=[
            "id",
            "standing ovation",
            "mean",
            "median",
            "variance",
            "standard deviation",
            "sentence count",
        ]
    )
    all_files = glob.glob("{}/{}/*".format(base_path, speech_type))
    for idx, file_path in tqdm(enumerate(all_files)):
        file_basename = os.path.basename(file_path)
        speech_id = re.findall(r"\d+", file_basename)[0]
        files_path = "{}/{}/{}.txt".format(base_path, speech_type, speech_id)
        sentences = preprocess(file_path)
        tokens_list = [nlp.rm(nlp.tokens(s)) for s in sentences]
        counts = [len(token) for token in tokens_list]
        mean_value = round(mean(counts), 2)
        median_value = round(median(counts), 2)
        variance_value = round(variance(counts), 2)
        stdev_value = round(stdev(counts), 2)

        df.loc[idx] = [
            speech_id,
            standing_ovation,
            round(mean(counts), 2),
            round(median(counts), 2),
            round(variance(counts), 2),
            round(stdev(counts), 2),
            len(sentences),
        ]

    df.to_csv("{}_sentence_stats.csv".format(speech_type), index=False)
