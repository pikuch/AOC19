# AOC19 main


def run_day(n):
    module_name = f"Day{n:02d}"
    try:
        module = __import__(module_name)
    except ModuleNotFoundError:
        print(f"Can't find {module_name}")
        exit(404)
    module.run()


def create_all_files():
    for i in range(1, 26):
        f_name = f"Day{i:02d}"
        with open(f_name + ".py", "w") as f:
            f.write(f"# AOC19 day {i:02d}\n\n\n")
            f.write("def load_data(f_name):\n")
            f.write("    with open(f_name, \"r\") as f:\n")
            f.write("        data_read = f.read()\n")
            f.write("    return data_read\n\n\n")
            f.write("def run():\n")
            f.write(f"    data = load_data(\"Day{i:02d}.txt\")\n\n")

        with open(f_name + ".txt", "w") as f:
            f.write("")
        with open(f_name + "test.txt", "w") as f:
            f.write("")


if __name__ == '__main__':
    run_day(25)
