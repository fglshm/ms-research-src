"""
    Let's search "not ~ but syntax" !!!
"""

from preprocessor import preprocess
import glob

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
