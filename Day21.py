# AOC19 day 21
from springDroid import SpringDroid
from itertools import product
import random


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def score(code, data):
    droid = SpringDroid(data)
    result, win = droid.run_and_score(code)
    if win:
        print(f"Found the code: {code}")
        print(f"Found the answer: {win}")
        exit(0)
    else:
        return result


def generate_random_code():
    instructions = ["AND", "OR", "NOT"]
    parameters1 = ["T", "J", "A", "B", "C", "D", "E", "F", "G", "H", "I"]
    parameters2 = ["T", "J"]
    return [[random.choice(instructions), random.choice(parameters1), random.choice(parameters2)] for _ in range(15)]


def choose_one(pop, pop_count):
    return pop[int(pop_count * (random.random() * random.random()))][0]


def crossover(a, b):
    place = random.randrange(1, 14)
    return a[:place] + b[place:], b[:place] + a[place:]


def mutate(a):
    instructions = ["AND", "OR", "NOT"]
    parameters1 = ["T", "J", "A", "B", "C", "D", "E", "F", "G", "H", "I"]
    parameters2 = ["T", "J"]
    b = a.copy()
    b[random.randrange(15)] = [random.choice(instructions), random.choice(parameters1), random.choice(parameters2)]
    return b


def rotate(a):
    place = random.randrange(1, 14)
    return a[place:] + a[:place]


# why think when you can use evolution
def find_running_codes(data, pop_count):
    pop = []
    # #151k
    # first = [['OR', 'F', 'J'], ['OR', 'F', 'J'], ['OR', 'F', 'J'], ['OR', 'G', 'J'], ['OR', 'F', 'J'], ['NOT', 'A', 'J'], ['OR', 'B', 'T'], ['AND', 'F', 'T'], ['OR', 'I', 'J'], ['OR', 'G', 'J'], ['OR', 'C', 'T'], ['AND', 'A', 'T'], ['AND', 'B', 'T'], ['NOT', 'T', 'J'], ['AND', 'D', 'J']]
    # pop.append([first, score(first, data)])

    # #99k
    # first = [['OR', 'H', 'J'], ['OR', 'E', 'J'], ['OR', 'E', 'J'], ['OR', 'H', 'J'], ['OR', 'E', 'J'], ['OR', 'G', 'J'], ['OR', 'I', 'J'], ['OR', 'H', 'J'], ['NOT', 'A', 'J'], ['OR', 'E', 'J'], ['OR', 'E', 'J'], ['OR', 'H', 'J'], ['OR', 'E', 'J'], ['AND', 'D', 'J'], ['OR', 'J', 'J']]
    # pop.append([first, score(first, data)])

    # the solution
    first = [['OR', 'F', 'J'], ['OR', 'F', 'J'], ['OR', 'F', 'J'], ['OR', 'H', 'J'], ['OR', 'F', 'J'], ['OR', 'F', 'J'],
     ['OR', 'B', 'T'], ['NOT', 'H', 'T'], ['OR', 'I', 'J'], ['OR', 'G', 'J'], ['OR', 'C', 'T'], ['AND', 'A', 'T'],
     ['AND', 'B', 'T'], ['NOT', 'T', 'J'], ['AND', 'D', 'J']]
    pop.append([first, score(first, data)])

    while len(pop) < pop_count:
        code = generate_random_code()
        pop.append([code, score(code, data)])
    pop.sort(key=lambda a: a[1], reverse=True)

    gen = 0
    while True:
        gen += 1
        print(f"Generation {gen}, best: {pop[0][1]} {pop[0][0]}")
        new_pop = []
        new_pop.extend(pop[:2])  # two top solutions stay
        while len(new_pop) < pop_count // 3:
            new_code1, new_code2 = crossover(choose_one(pop, pop_count), choose_one(pop, pop_count))
            new_pop.append([new_code1, score(new_code1, data)])
            new_pop.append([new_code2, score(new_code2, data)])
        while len(new_pop) < pop_count * 2 // 3:
            new_code = mutate(choose_one(pop, pop_count))
            new_pop.append([new_code, score(new_code, data)])
        while len(new_pop) < pop_count:
            new_code = rotate(choose_one(pop, pop_count))
            new_pop.append([new_code, score(new_code, data)])
        pop = new_pop
        pop.sort(key=lambda a: a[1], reverse=True)


def run():
    data = load_data("Day21.txt")
    droid = SpringDroid(data)
    # figured out with a brain: ["OR D J", "OR A T", "AND B T", "AND C T", "NOT T T", "AND T J"]
    code4 = ["OR D J", "OR A T", "AND B T", "AND C T", "NOT T T", "AND T J"]
    output = droid.walk(code4)
    for c in output:
        if c < 256:
            print(chr(c), end="")
        else:
            print(c)

    # genetic algorithm used to find the right code:
    # find_running_codes(data, 60)

    droid = SpringDroid(data)
    code9 = [['OR', 'H', 'J'], ['OR', 'F', 'J'], ['OR', 'I', 'J'], ['OR', 'G', 'J'],
             ['OR', 'B', 'T'], ['NOT', 'H', 'T'], ['OR', 'C', 'T'], ['AND', 'A', 'T'],
             ['AND', 'B', 'T'], ['NOT', 'T', 'J'], ['AND', 'D', 'J']]
    output = droid.run(code9)
    for c in output:
        if c < 256:
            print(chr(c), end="")
        else:
            print(c)
