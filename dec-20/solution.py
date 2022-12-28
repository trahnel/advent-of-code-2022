import time

# TEST = True
TEST = False

filepath = "test.txt" if TEST else "input.txt"

with open(filepath, 'r') as f:
    data = list(map(int, [line.strip() for line in f.readlines()]))

print(data)

sequence = [(x, i) for i, x in enumerate(data)]


def move_num(i, seq):
    val, old_pos = seq[i]

    seq_len = len(seq)

    steps = -(abs(val) % (seq_len - 1)) if val < 0 else abs(val) % (seq_len - 1)

    new_pos = old_pos + steps
    if new_pos < 1:
        new_pos = seq_len + new_pos - 1
    elif new_pos > (seq_len - 1):
        new_pos = new_pos - seq_len + 1

    if new_pos > old_pos:
        seq = [(v, p - 1 if old_pos < p <= new_pos else p) for v, p in seq]
    else:
        seq = [(v, p + 1 if new_pos <= p < old_pos else p) for v, p in seq]

    seq[i] = val, new_pos

    # sorted_seq = sorted(seq.copy(), key=lambda x: x[1])
    # assert all((sorted_seq[i - 1][1] + 1 == sorted_seq[i][1]) for i in range(1, len(sorted_seq)))
    return seq


def find_wrap_num(i, seq):
    seq_len = len(seq)
    zero_index = seq.index(0)
    before_rounds = i - (seq_len - zero_index - 1)
    round_count = before_rounds // seq_len
    after_rounds = before_rounds - round_count * seq_len
    return seq[after_rounds - 1]


def run_part1():
    start = time.time()

    seq = sequence
    seq_len = len(seq)
    for i, _ in enumerate(seq):
        print("{}/{}".format(i + 1, seq_len))
        seq = move_num(i, seq)

    seq = sorted(seq, key=lambda x: x[1])
    seq = [v for v, p in seq]
    part1 = find_wrap_num(1000, seq) + find_wrap_num(2000, seq) + find_wrap_num(3000, seq)

    print("Part 1: {}, {:0.2f}s".format(part1, time.time() - start))
    if TEST:
        assert part1 == 3
    else:
        assert part1 == 10831


run_part1()


def run_part2():
    start = time.time()

    seq = sequence
    seq = [(x * 811589153, i) for x, i in seq]

    for m in range(10):
        print("Round", m + 1)
        for i, _ in enumerate(seq):
            seq = move_num(i, seq)

    seq = sorted(seq, key=lambda x: x[1])
    seq = [v for v, p in seq]
    part2 = find_wrap_num(1000, seq) + find_wrap_num(2000, seq) + find_wrap_num(3000, seq)

    print("Part 1: {}, {:0.2f}s".format(part2, time.time() - start))
    if TEST:
        assert part2 == 1623178306
    else:
        assert part2 == 6420481789383


run_part2()
