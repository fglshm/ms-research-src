"""
    卒論時に、SO でも NSO でもなく、チェックできなかったスピーチを取得するコード
"""


import re


def remove_double_empty(lst):
    """
    連続した空白を削除
    """
    return [re.sub(r'\s+', r' ', elem) for elem in lst]


def leave_only_chara_and_number(lst):
    """
        記号と数字以外を空白に変換し、要素を小文字に変換
    """
    return [re.sub(r'[^a-z0-9\s]', r'', elem.lower().strip()) for elem in lst]


all_speeches = open('../data/all_titles.txt').read().strip().split('\n')
so_speeches = open('../data/so_titles.txt').read().strip().split('\n')
nso_speeches = open('../data/nso_titles.txt').read().strip().split('\n')


all_speeches = remove_double_empty(leave_only_chara_and_number(all_speeches))
so_speeches = remove_double_empty(leave_only_chara_and_number(so_speeches))
nso_speeches = remove_double_empty(leave_only_chara_and_number(nso_speeches))

for so in so_speeches:
    if so in all_speeches:
        all_speeches.remove(so)

for nso in nso_speeches:
    if nso in all_speeches:
        all_speeches.remove(nso)


with open('../data/unable_checked_speech_titles.txt', 'a') as f:
    for speech in all_speeches:
        f.write('%s\n' % speech)

# a = [1, 2, 3, 4, 6, 7, 8, 9]
# b = [2, 4, 5]
# c = [1, 3]

# for elem in b:
#     a.remove(elem)

# for elem in c:
#     a.remove(elem)

# print(a)
