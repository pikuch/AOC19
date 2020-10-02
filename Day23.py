# AOC19 day 23
from network import Network


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day23.txt")
    net = Network(50, data)
    x, y = net.simulate(stop_on_255=True)
    print(f"The first packet sent to address 255 is {x}, {y}")

    net = Network(50, data)
    x, y = net.simulate()
    print(f"The first packet sent from NAT twice is {x}, {y}")
