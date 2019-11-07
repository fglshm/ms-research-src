import glob

path = '/Users/shohei/Tsukuba/tsukuba/research/master/dataset/similarity/sentence/word_count/diff/60seconds'
dirs = glob.glob(f'{path}/*')
child_files = [glob.glob(f'{dir}/max/*') for dir in dirs]
[print(len(files)) for files in child_files]
