import pandas as pd

df = pd.read_csv('result_stats.csv', header=0, index_col=0)

ratios = df['SO/NSO']
acc = df['正解率']
f = df['F値']

ratios_s = pd.Series(ratios)
acc_s = pd.Series(acc)
f_s = pd.Series(f)

corr_ratio_acc = ratios_s.corr(acc_s)
corr_ratio_f = ratios_s.corr(f_s)
print(f'SO/NSO と 正解率の相関係数: {corr_ratio_acc}')
print(f'SO/NSO と F値の相関係数: {corr_ratio_f}')
