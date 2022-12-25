import time

# TEST = True
TEST = False

filepath = "test.txt" if TEST else "input.txt"

with open(filepath, 'r') as f:
    data = [line.strip() for line in f.readlines()]

print(data)


def snafu2dec(snafu):
    dec = 0
    for i, x in enumerate(reversed(snafu)):
        if x == "-":
            dec += int("1" + "0" * i, 5) * -1
        elif x == "=":
            dec += int("1" + "0" * i, 5) * -2
        else:
            dec += int(x + "0" * i, 5)
    return dec


assert snafu2dec("1") == 1
assert snafu2dec("1=") == 3
assert snafu2dec("1-") == 4
assert snafu2dec("2=-01") == 976
assert snafu2dec("1=11-2") == 2022
assert snafu2dec("1121-1110-1=0") == 314159265


def dec2snafu(dec):
    snafu = ""
    while dec != 0:
        q, r = divmod(dec + 2, 5)
        snafu += "=-012"[r]
        dec = q
    return snafu[::-1]


assert dec2snafu(1) == "1"
assert dec2snafu(2) == "2"
assert dec2snafu(3) == "1="
assert dec2snafu(5) == "10"
assert dec2snafu(6) == "11"
assert dec2snafu(7) == "12"
assert dec2snafu(10) == "20"
assert dec2snafu(12) == "22"


def run_part1():
    start = time.time()

    part1_dec = sum([snafu2dec(x) for x in data])
    part1 = dec2snafu(part1_dec)
    print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start))
    if TEST:
        assert part1 == "2=-1=0"
    else:
        assert part1 == "2-=102--02--=1-12=22"


run_part1()
