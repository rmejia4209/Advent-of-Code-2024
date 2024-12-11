from utils.utils import get_raw_input_stream

Numbers = list[int]


def convert_to_numbers(data: str) -> Numbers:
    """Converts string data to list of numbers"""
    return [int(num) for num in data.split(" ")]


def has_even_digits(num: int) -> bool:
    """Returns true if the number has an even number of digits"""
    if len(str(num)) % 2 == 0:
        return True
    return False


def split_in_half(num: int) -> tuple[int, int]:
    num = str(num)
    mid_point = int(len(num) / 2)
    return int(num[:mid_point]), int(num[mid_point:])


def apply_rules(stones: Numbers) -> Numbers:
    """Applies the rules after blinking once"""
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif has_even_digits(stone):
            new_stones.extend(list(split_in_half(stone)))
        else:
            new_stones.append(stone * 2024)
    return new_stones


def blink(stones_map: dict[int, int]) -> Numbers:
    """Applies the rules after blinking once"""
    stones = [
        stone for stone in stones_map.keys() if stones_map[stone]['count'] > 0
    ]
    cache = {}
    for stone in stones:
        if not stones_map[stone].get('turns_into'):
            stones_map[stone]['turns_into'] = apply_rules([stone])
        for new_stone in stones_map[stone]['turns_into']:
            count = stones_map[stone]['count']
            cache[new_stone] = cache.get(new_stone, 0) + count
        stones_map[stone]['count'] = 0
    for new_stone in cache.keys():
        if not stones_map.get(new_stone):
            stones_map[new_stone] = {'count': cache[new_stone]}
        else:
            stones_map[new_stone]['count'] += cache[new_stone]
    return


def multiple_blinks(stones: Numbers, blinks: int) -> int:
    """Blinks multiple times"""
    cache = {}
    for stones in stones:
        cache[stones] = {'count': 1}

    for _ in range(blinks):
        blink(cache)

    return sum([cache[stone]['count'] for stone in cache.keys()])


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    stones = convert_to_numbers(get_raw_input_stream(11))
    sol_1 = multiple_blinks(stones, 25)
    stones = convert_to_numbers(get_raw_input_stream(11))
    sol_2 = multiple_blinks(stones, 75)
    return sol_1, sol_2
