# AOC19 day 04

def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def count_passwords(digits, has_pair, val_range):
    if len(digits) == 6:
        if has_pair and val_range[0] <= digits <= val_range[1]:
            return 1
        else:
            return 0
    counter = 0 if digits == "" else count_passwords(digits + digits[-1], True, val_range)
    last_digit = ord("1") if digits == "" else ord(digits[-1]) + 1
    for d in range(last_digit, ord("9") + 1):
        counter += count_passwords(digits + chr(d), has_pair, val_range)
    return counter


def count_passwords2(digits, counts, val_range):
    if len(digits) == 6:
        if 2 in counts and val_range[0] <= digits <= val_range[1]:
            return 1
        else:
            return 0
    counter = 0
    last_digit = ord("1") if digits == "" else ord(digits[-1])
    for d in range(last_digit, ord("9") + 1):
        new_counts = counts[:]
        new_counts[int(chr(d))] += 1
        counter += count_passwords2(digits + chr(d), new_counts, val_range)
    return counter


def run():
    data = load_data("Day04.txt")
    val_range = data.split("-")
    pass_count = count_passwords("", False, val_range)
    print(f"{pass_count} passwords within the range meet these criteria")
    pass_count2 = count_passwords2("", [0]*10, val_range)
    print(f"{pass_count2} passwords within the range meet these criteria")
