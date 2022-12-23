import time

from sympy import symbols, solve

# TEST = True
TEST = False

filepath = "test.txt" if TEST else "input.txt"

with open(filepath, 'r') as f:
    yells_data = [line.strip().split(": ") for line in f.readlines()]

yells = {x[0]: x[1] for x in yells_data}


# print(yells)


def get_yell(m):
    if m in ["+", "-", "*", "/", "=", "x"]:
        return m

    m_yell = yells[m]
    if m_yell.isnumeric():
        return m_yell
    else:
        s = "("
        yell_parts = m_yell.split()
        for p in yell_parts:
            s += get_yell(p)
        return s + ")"


def run_part1():
    start = time.time()

    final_yell = get_yell("root")
    part1 = round(eval(final_yell))
    print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start))
    if TEST:
        assert part1 == 152
    else:
        assert part1 == 21208142603224


run_part1()


def run_part2():
    start = time.time()

    root_yell = yells["root"].split()
    yells["root"] = root_yell[0] + " = " + root_yell[2]
    yells["humn"] = "x"

    yell = get_yell("root")[1:-1]
    l, r = yell.split("=")

    x = symbols('x')
    part2 = round(solve(eval(l) - eval(r))[0])
    print("Part 2: {}, {:0.2f}s".format(part2, time.time() - start))

    if TEST:
        assert part2 == 301
    else:
        assert part2 == 3882224466191


run_part2()
