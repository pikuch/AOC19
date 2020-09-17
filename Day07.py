# AOC19 day 07
from intcode import Intcode
from itertools import permutations


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def test_phase_settings(data):
    amplis = []
    for i in range(5):
        amplis.append(Intcode())
    max_output = 0
    for phases in permutations(range(5)):
        signal = 0
        for i in range(5):
            amplis[i].load(data)
            amplis[i].inputs.append(phases[i])
            amplis[i].inputs.append(signal)
            amplis[i].run()
            signal = amplis[i].outputs.popleft()
        if signal > max_output:
            max_output = signal
    return max_output


def run():
    data = load_data("Day07.txt")
    max_signal = test_phase_settings(data)
    print(f"The maximum signal that can be produced is {max_signal}")
