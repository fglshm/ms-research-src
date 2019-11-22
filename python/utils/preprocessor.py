import re


def preprocess(file_path):
    """
        Preprocess text by removing unecessary characters
        and return the sentence list
    """
    text = open(file_path).read().strip().replace('"', "")
    text = re.sub(r"(Dr|Mr|Mrs|Prof|Professor)\.", r"\1", text) # replace . to empty chara
    text = re.sub(r"\s\—+\s|\,|\:|\s\.+\s", r"", text) # --- や カンマ (,) や コロン (:) などを削除
    text = re.split(r"[\.\!\?]\s", text) # ピリオド, びっくり, クエスチョンで分割 -> 文単位に変換
    sentence_list = list(map(lambda x: re.sub(r"\(.+\)", r"", x), text)) # Applause, Laughter などを削除
    sentence_list = list(map(lambda x: x.strip(), sentence_list)) # 先頭末尾の空白を削除
    sentence_list = list(map(lambda x: re.sub(r"\s+", r" ", x), sentence_list)) # 連続する空白を削除
    sentence_list = [elem for elem in sentence_list if elem] # 空白要素を削除
    return sentence_list
