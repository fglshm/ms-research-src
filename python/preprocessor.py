import re


def preprocess(file_path):
    """
        Preprocess text by removing unecessary characters
        and return the sentence list
    """
    text = open(file_path).read().strip().replace('"', "")
    text = re.sub(r"(Dr|Mr|Mrs|Prof|Professor)\.", r"\1", text)
    text = re.sub(r"\s\—+\s|\,|\:|\s\.+\s", r"", text)
    text = re.split(r"[\.\!\?]\s", text)
    sentence_list = list(map(lambda x: re.sub(r"\(.+\)", r"", x), text))
    sentence_list = list(map(lambda x: x.strip(), sentence_list))
    sentence_list = list(map(lambda x: re.sub(r"\s+", r" ", x), sentence_list))
    sentence_list = [elem for elem in sentence_list if elem]
    return sentence_list
