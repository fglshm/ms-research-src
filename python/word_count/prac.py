import numpy as np


def get_frequency(lst):
    """
        度数を求めてそのリストを返す
    """
    frequency = np.zeros(10)
    for elem in lst:
        idx = int(elem)
        frequency[idx] += 1
    return frequency


def main():
    lst = np.array([
        0.2, 0.7, 1.3, 2.9, 3.2, 3.3,
        3.9, 4.1, 5.6, 7.1, 8.2, 8.9, 9.1
    ])
    frequency = get_frequency(lst)
    f = np.zeros(10)
    f = np.add(f, frequency)
    print(f)
    lst2 = np.array([
        1.2, 2.7, 2.3, 2.9, 3.2, 3.3,
        3.9, 5.1, 5.6, 7.1, 7.2, 8.9, 9.1
    ])
    frequency2 = get_frequency(lst2)
    print(frequency2)
    f = np.add(f, frequency2)
    print(f)


if __name__ == "__main__":
    main()
