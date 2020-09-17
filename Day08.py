# AOC19 day 08
import numpy as np


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_space_image(data, width, height):
    return np.array(list(data), dtype=np.uint8).reshape((-1, height, width))


def layer_det(image):
    layer_number = np.argmin(np.sum(image == 0, axis=(1, 2)))
    layer = image[layer_number, :, :]
    return np.sum(layer == 1) * np.sum(layer == 2)


def decode_image(image):
    for h in range(image.shape[1]):
        for w in range(image.shape[2]):
            for layer in range(image.shape[0]):
                if image[layer, h, w] != 2:
                    if image[layer, h, w] == 1:
                        print("█", end="")
                    else:
                        print("░", end="")
                    break
        print()


def run():
    data = load_data("Day08.txt")
    width, height = 25, 6
    image = parse_space_image(data, width, height)
    print(f"The number of 1s times the number of 2s in the layer with fewest 0s is {layer_det(image)}")
    decode_image(image)
