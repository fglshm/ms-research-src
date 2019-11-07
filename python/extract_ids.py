"""
    SO/NSO の speech_id を抽出
"""

import glob
import pandas as pd

speech_types = ['so', 'nso']
for speech_type in speech_types:
    print(speech_type)
    csv_file = f'{speech_type}_sentence_stats.csv'
    df = pd.read_csv(csv_file)
    df = df.sort_values(by=['id'])
    with open(f'{speech_type}_ids.txt', 'w') as f:
        for id in df['id']:
            f.write(f'{str(id)}\n')
