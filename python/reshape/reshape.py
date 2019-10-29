"""
    トピック名, SO, NSO, SO/NSO, 正解率, F値
    を出力する
"""
import re
import csv

so_nso_count_file = open('so_nso_count.txt').read().strip().split('\n')

topics = []
so_counts = []
nso_counts = []
ratios = []

for elem in so_nso_count_file:
    topic_pattern = '[\D\s]+'
    elem = elem.strip()
    topic = re.match(topic_pattern, elem).group().strip()
    so_count = int(re.findall(r'\d+', elem)[0])
    nso_count = int(re.findall(r'\d+', elem)[1])
    if so_count + nso_count >= 100:
        topics.append(topic)
        so_counts.append(so_count)
        nso_counts.append(nso_count)
        ratios.append(round(so_count/nso_count, 2))


accuracy_file = open('accuracy.txt').read().strip().split('\n')
accuracy_dictionaries = {}
for elem in accuracy_file:
    topic = re.match(topic_pattern, elem).group().strip()
    acc = re.findall(r'[\d\.]+', elem)[0]
    accuracy_dictionaries[topic] = round(float(acc), 3)

f_score_file = open('f_score.txt').read().strip().split('\n')
f_score_dictionaries = {}
for elem in f_score_file:
    topic = re.match(topic_pattern, elem).group().strip()
    f = re.findall(r'[\d\.]+', elem)[0]
    f_score_dictionaries[topic] = round(float(f), 2)


# with open('result_stats.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow('トピック,SO,NSO,SO/NSO,正解率,F値'.split(','))
#     for topic, so, nso, ratio in zip(topics, so_counts, nso_counts, ratios):
#         result = f'{topic},{so},{nso},{ratio},{accuracy_dictionaries[topic]},{f_score_dictionaries[topic]}'
#         writer.writerow(result.split(','))
