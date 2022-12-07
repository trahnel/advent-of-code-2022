# filepath = 'test.txt'
filepath = 'input.txt'

with open(filepath, 'r') as f:
    data = [x.strip() for x in f.readlines()]


# print(data)


class Dir:
    def __init__(self, name, parent=None):
        self.name = name
        self.dirs = []
        self.files = []
        self.size = 0
        self.parent = parent

    def __repr__(self):
        return repr("- {} (dir, size={})".format(self.name, self.size))


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return repr("- {} (file, size={})".format(self.name, self.size))


def get_is_cmd(x):
    return x.startswith('$ ')


def get_is_cmd_cd(x):
    if x.startswith('$ cd'):
        return True, x.removeprefix('$ cd ')
    return False, None


def get_is_cmd_ls(x):
    if x.startswith('$ ls'):
        return True
    return False


def get_dir_content(input):
    cmds = [i for i in range(0, len(input)) if data[i].startswith('$')]
    if not cmds:
        return input, []

    content_length = cmds[0]
    content = input[:content_length]
    input_rest = input[content_length:]
    return content, input_rest


def get_cd_dir_pointer(parent, dir_name):
    for d in parent.dirs:
        if d.name == dir_name:
            return d


def add_content(parent, content):
    p = parent
    for c in content:
        parent = p
        if c.startswith('dir'):
            d = Dir(c.split()[1], parent)
            parent.dirs.append(d)
        else:
            size, name = c.split()
            f = File(name, int(size))
            parent.files.append(f)
            while parent:
                parent.size += int(size)
                parent = parent.parent


root = Dir('/')
tree = {root}
pointer = None

while data:
    line = data.pop(0)
    is_cmd = get_is_cmd(line)
    # print(line)

    if is_cmd:
        is_cd, d = get_is_cmd_cd(line)

        if is_cd:
            if d == '/':
                pointer = root
            elif d == '..':
                pointer = pointer.parent
            else:
                pointer = get_cd_dir_pointer(pointer, d)
        elif get_is_cmd_ls(line):
            content, data_rest = get_dir_content(data)
            data = data_rest
            add_content(pointer, content)


def get_dirs(d):
    dirs = [d]
    for dr in d.dirs:
        dirs.extend(get_dirs(dr))
    return dirs


dirs = get_dirs(root)

part1 = sum([d.size for d in dirs if d.size <= 100000])
assert part1 == 1792222
print("Part 1:", part1)

unused = 70000000 - root.size
required = 30000000 - unused

part2 = None
dirs.sort(key=lambda x: x.size)
for d in dirs:
    if d.size > required:
        part2 = d.size
        break
assert part2 == 1112963
print("Part 2:", part2)
