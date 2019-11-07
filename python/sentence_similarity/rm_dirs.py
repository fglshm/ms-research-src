import shutil
import glob
import os

path = '/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/diff/60seconds'
dirs = [f'{dir}/5' for dir in glob.glob(f'{path}/*')]
for dir in dirs:
    if os.path.exists(dir):
        shutil.rmtree(dir)
