# AOC19 day 16
import numpy as np


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def get_coefficient(row, col):
    pos = ((col + 1) // (row + 1)) % 4
    return 1 - abs(pos - 1)


def fft(code, n):
    coeffs = np.fromfunction(lambda row, col: get_coefficient(row, col), (len(code), len(code)), dtype=np.int)
    for _ in range(n):
        code = np.abs(np.dot(coeffs, code)) % 10
    return code


# takes a few seconds to run
def fft_10k(code, n):
    for step in range(n):
        new_code = [0]*len(code)
        the_sum = 0
        for i in reversed(range(len(code))):
            the_sum += code[i]
            new_code[i] = (abs(the_sum) % 10)
        code = new_code
        print(f"\r{step + 1}/{n}", end="")
    print(" done.")
    return code


# faster with numpy
def fft_10k_numpy(code, n):
    code = np.array(code[::-1])
    for step in range(n):
        code = np.abs(np.cumsum(code)) % 10
        print(f"\r{step + 1}/{n}", end="")
    print(" done.")
    return code[::-1]


def run():
    data = load_data("Day16.txt")
    code = list(map(int, list(data)))

    code = fft(code, 100)
    print("".join(map(str, code))[:8])

    # part 2

    offset = int(data[:7])
    data2 = data*10000
    code2 = list(map(int, list(data2[offset:])))
    code2 = fft_10k_numpy(code2, 100)
    print("".join(map(str, code2))[:8])
    # 37615297
