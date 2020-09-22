# AOC19 day 16
import numpy as np


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def get_coefficients(row, col):
    pos = ((col + 1) // (row + 1)) % 4
    return 1 - abs(pos - 1)


def fft(code, n):
    coeffs = np.fromfunction(lambda row, col: get_coefficients(row, col), (len(code), len(code)), dtype=np.int)
    for _ in range(n):
        code = np.abs(np.dot(coeffs, code)) % 10
    return code


def run():
    data = load_data("Day16.txt")
    code = list(map(int, list(data)))

    code = fft(code, 100)
    print("".join(map(str, code))[:8])
