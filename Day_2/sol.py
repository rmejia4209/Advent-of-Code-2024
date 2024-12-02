from utils.utils import extract_data


def convert_to_ints(data: list[str]) -> list[list[int]]:
    """
    Converts the input from a list of strings to a list of a list of ints
    """

    converted_data = []
    for line in data:
        converted_data.append([int(num) for num in line.split(" ")])
    return converted_data


def calc_diff(data: list[int]) -> list[int]:
    """
    Returns a list of differences between each number in the given argument
    """
    seq_diff = []
    # Iterate through the sequence up until the last value
    for idx in range(len(data)-1):
        seq_diff.append(data[idx] - data[idx+1])
    return seq_diff


def create_diff_array(data: list[list[int]]) -> list[list[int]]:
    """Returns a list of difference lists"""
    diff = []
    # Iterate through each sequence of numbers
    for seq in data:
        diff.append(calc_diff(seq))
    return diff


def safely_changing(data: list[int], lower: int, upper: int) -> bool:
    """
    Returns the true if the number of difference within the bounds is 
    the same as the length of the input.
    """
    return len(data) == len([x for x in data if (lower <= x <= upper)])


def is_tolerable(data: list[int]) -> bool:
    """
    Returns true if data only contains one valid that makes it unsafe.
    Currently implements a brute force solution.
    """
    for skipped_idx in range(len(data)):
        temp = []
        for idx in range(len(data)):
            if idx != skipped_idx:
                temp.append(data[idx])
        temp = calc_diff(temp)
        if safely_changing(temp, 1, 3) or safely_changing(temp, -3, -1):
            return True
    return False


def determine_safe_reports(data: list[list[int]]) -> tuple[int, int]:
    """
    Returns the number of sequences that do not oscillate and
    do not change by more than 2 at any given step along with the number
    of sequences that are tolerable.
    """
    total = 0
    tolerable = 0
    differences = create_diff_array(data)

    for seq, diff in zip(data, differences):
        if safely_changing(diff, 1, 3) or safely_changing(diff, -3, -1):
            total += 1
        elif is_tolerable(seq):
            tolerable += 1

    return total, tolerable+total


def solution() -> tuple[int, int]:
    data = convert_to_ints(extract_data(2))
    num_safe_reports, tolerable_reports = determine_safe_reports(data)
    return num_safe_reports, tolerable_reports
