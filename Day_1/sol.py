from utils.utils import extract_data


def split_data(
    data: list[str],
    deliminator: str = " ",
) -> tuple[list[int], list[int]]:
    """
    Returns a tuple of list of integers. The data is split line by line by
    the deliminator
    """
    left: list[int] = []
    right: list[int] = []

    for line in data:
        line_split = line.split(deliminator)
        left.append(int(line_split[0]))
        right.append(int(line_split[-1]))

    return left, right


def calc_diff(left: list[int], right: list[int]) -> int:
    """
    Returns the sum of differences between each pair of numbers in both list.
    Sorts the the list in place.
    """
    left.sort()
    right.sort()
    total_diff = 0
    for left_val, right_val in zip(left, right):
        total_diff += abs(left_val - right_val)
    return total_diff


def create_freq_map(nums: list[int]) -> dict[int, int]:
    """
    Returns a dictionary with each unique number as a key its
    frequency in the list as the value
    """
    freq_map = {}
    for num in nums:
        freq_map[num] = freq_map.get(num, 0) + 1
    return freq_map


def calc_similarity(left: list[int], right: list[int]) -> int:
    """
    Returns similarity score that is calculated multiplying each number
    in one list number by its frequency in the other list and summing
    each operation
    """
    freq_map = create_freq_map(right)

    similarity = 0
    for num in left:
        similarity += (num * freq_map.get(num, 0))
    return similarity


def solution() -> tuple[int, int]:
    """Returns the solutions for Day 1 of Advent of Code"""
    data = extract_data(1)
    left, right = split_data(data)
    solution_1 = calc_diff(left, right)
    solution_2 = calc_similarity(left, right)

    return solution_1, solution_2
