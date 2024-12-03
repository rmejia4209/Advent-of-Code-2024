import re
from utils.utils import get_raw_input_stream


def get_all_muls(txt: str) -> list[str]:
    """
    Finds all of the regex matches in the given txt

    Regex = mul(/d{1-3},/d{1-3}) ~ basically mul() and two 1 - 3
    digit numbers separated with a comma
    """
    regex = r"(?:mul)\(\d{1,3}\,\d{1,3}\)"
    return re.findall(regex, txt)


def get_all_ops(txt: str) -> list[str]:
    """
    Finds all of the regex matches in the given txt. Finds mul, do, don't
    operations.
    """
    rgx = r"(?:(?:mul)\(\d{1,3}\,\d{1,3}\))|(?:(?:do)\(\))|(?:(?:don\'t)\(\))"
    return re.findall(rgx, txt)


def filter_operations(data: list[str]) -> list[str]:
    """
    Removes the do() and don't() commands from the list along with any
    mul() operation following a don't() command.
    """
    valid_operations = []
    add_operations = True
    for op in data:
        if op == "do()":
            add_operations = True
        elif op == "don't()":
            add_operations = False
        elif add_operations:
            valid_operations.append(op)
    return valid_operations


def get_nums(txt: str) -> tuple[int, int]:
    """Returns the pair of numbers found in mul(x,y)"""
    regex = r"\d{1,3}"
    num_1, num_2 = re.findall(regex, txt)
    return int(num_1), int(num_2)


def generate_nums_list(data: list[str]) -> list[tuple[int, int]]:
    """Returns the pairs of numbers found in the list of strings"""
    nums = []
    for operation in data:
        nums.append(get_nums(operation))
    return nums


def sum_product(data: list[tuple[int, int]]) -> int:
    """Returns the sum product of the given input"""
    sum_product = 0
    for num_1, num_2 in data:
        sum_product += num_1 * num_2
    return sum_product


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    raw_data = get_raw_input_stream(3)

    # Find all valid mul operations
    matches = get_all_muls(raw_data)
    data = generate_nums_list(matches)
    sol_1 = sum_product(data)

    # Find all valid mul operations considering do() and don't()
    matches = get_all_ops(raw_data)
    matches = filter_operations(matches)
    data = generate_nums_list(matches)
    sol_2 = sum_product(data)

    return sol_1, sol_2
