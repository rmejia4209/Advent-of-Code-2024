from utils.utils import extract_data_to_list_of_list

Point = tuple[int, int]
AntennaMap = dict[str, list[Point]]


def get_antenna_map(data: list[list[str]]) -> AntennaMap:
    """
    Returns a dictionary with each type of antenna as a key and
    their locations stored in a list as tuples
    """
    antenna_map = {}
    for row in range(len(data)):
        for col in range(len(data[row])):
            char = data[row][col]
            if char != '.':
                location = (row, col)
                antenna_map.setdefault(char, []).append(location)
    return antenna_map


def get_sol_1(data: list[list[str]]) -> int:
    """Wrapper function to get solution 1"""
    antenna_map = get_antenna_map(data)
    return


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    data = extract_data_to_list_of_list(8)
    sol_1 = get_sol_1(data)

    return sol_1, None
