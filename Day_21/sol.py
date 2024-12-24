from itertools import permutations, product
from utils.utils import extract_data_to_list


Point = tuple[int, int]
Pad = list[list[str]]
Buttons = str
Paths = list[str]


def generate_all_button_pairs(pad: Pad) -> list[Buttons]:
    """Returns a list of all the possible button pairs on the given pad"""
    flatten = [btn for row in pad for btn in row if btn != '']
    return [''.join(pair) for pair in product(flatten, repeat=2)]


def get_btn_location(pad: Pad, target: str) -> Point:
    """Return the location of the button on the pad"""
    for row, btns in enumerate(pad):
        for col, btn in enumerate(btns):
            if btn == target:
                return row, col


def get_vertical_moves(start: Point, end: Point) -> str:
    """Returns the vertical moves needed"""
    diff = end[0] - start[0]
    if diff < 0:
        return abs(diff) * '^'
    return abs(diff) * 'v'


def get_horizontal_moves(start: Point, end: Point) -> str:
    """Returns the vertical moves needed"""
    diff = end[1] - start[1]
    if diff < 0:
        return abs(diff) * '<'
    return abs(diff) * '>'


def get_needed_moves(pad: Pad, btns: Buttons) -> str:
    """Return the needed moves from the one button the next"""
    start, end = get_btn_location(pad, btns[0]), get_btn_location(pad, btns[1])
    return get_vertical_moves(start, end) + get_horizontal_moves(start, end)


def get_val(pad: Pad, point: Point) -> int | str:
    """Return the value at the point"""
    row, col = point
    return pad[row][col]


def add_points(pt1: Point, pt2: Point) -> Point:
    """Adds pt1 and pt2"""
    r1, c1 = pt1
    r2, c2 = pt2
    return r1 + r2, c1 + c2


def is_path_valid(pad: Pad, path: str, start: Point):
    """Returns true if path does not go over empty string"""
    moves = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    curr_point = start
    for move in path:
        curr_point = add_points(curr_point, moves[move])
        if get_val(pad, curr_point) == '':
            return False
    return True


def get_paths(pad: list[list[str]], btns: Buttons):
    """
    Returns all possible paths on the pad from the first button
    to the second button
    """
    req_moves = get_needed_moves(pad, btns)
    possible_paths = set(''.join(path) for path in permutations(req_moves))
    start = get_btn_location(pad, btns[0])
    valid_paths = [
        path for path in possible_paths if is_path_valid(pad, path, start)
    ]
    return valid_paths


def calc_shortest_number_pad_path() -> dict[Buttons, Paths]:
    """
    Returns a list of the shortest sequences from each combinations
    of buttons on a number pad
    """
    num_pad = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        ['', '0', 'A']
    ]
    btn_pairs = generate_all_button_pairs(num_pad)
    return {btn_pair: get_paths(num_pad, btn_pair) for btn_pair in btn_pairs}


def calc_shortest_key_pad_path() -> dict[Buttons, Paths]:
    """
    Returns a list of the shortest sequences from each combinations
    of buttons on a number pad
    """
    key_pad = [
        ['', '^', 'A'],
        ['<', 'v', '>']
    ]
    btn_pairs = generate_all_button_pairs(key_pad)
    return {btn_pair: get_paths(key_pad, btn_pair) for btn_pair in btn_pairs}


def build_key_sequence(
    btns: str, idx: int, prev_btn: str, curr_path: str, paths: Paths,
    cache: dict[Buttons, Paths]
):
    """
    Builds a list of valid key sequences to enter the given button sequence
    """
    if idx == len(btns):
        paths.append(curr_path)
        return
    btn_pair = f'{prev_btn}{btns[idx]}'
    for path in cache[btn_pair]:
        build_key_sequence(
            btns, idx+1, btns[idx], curr_path + path + 'A', paths, cache
        )


def shortest_sequence(btns, depth, cache, best_key_pad_paths):
    """
    Returns the length of the of shortest sequence of buttons that need to be
    input at depth to achieve the given input (btns)
    """

    # base case
    if depth == 0:
        return len(btns)

    if (btns, depth) in cache:
        return cache[(btns, depth)]

    subs = [sub + 'A' for sub in btns.split('A')][:-1]
    total_len = 0
    for sub in subs:
        seq_list = []
        build_key_sequence(sub, 0, 'A', '', seq_list, best_key_pad_paths)
        seq_lens = []
        for seq in seq_list:
            seq_lens.append(
                shortest_sequence(seq, depth-1, cache, best_key_pad_paths)
            )
        total_len += min(seq_lens)
    cache[(btns, depth)] = total_len
    return total_len


def solve(codes: list[str], depth: int):
    """
    Harness function
    """

    best_num_pad_paths = calc_shortest_number_pad_path()
    best_key_pad_paths = calc_shortest_key_pad_path()
    cache = {}
    total = 0
    for code in codes:
        seq_list = []
        build_key_sequence(code, 0, 'A', '', seq_list, best_num_pad_paths)

        seq_lens = []
        for seq in seq_list:
            seq_lens.append(
                shortest_sequence(seq, depth, cache, best_key_pad_paths)
            )
        total += int(code[:-1])*min(seq_lens)
    return total


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    codes = extract_data_to_list(21)
    return solve(codes, 2), solve(codes, 25)
