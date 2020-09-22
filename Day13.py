# AOC19 day 13
from arcade import Arcade


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day13.txt")
    arcade = Arcade()
    arcade.load_game(data)
    arcade.run()
    arcade.draw_screen()
    print(f"The game drew {len([tile for tile in arcade.screen.values() if tile == 2])} tiles")
