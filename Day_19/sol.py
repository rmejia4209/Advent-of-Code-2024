from utils.utils import extract_data_to_list


def get_available_patterns(data: list[str]) -> list[str]:
    """Returns the available patterns. Removes patterns from data"""
    patterns = data[0].split(', ')
    data.pop(0)
    data.pop(0)
    return sorted(patterns, key=lambda pattern: len(pattern), reverse=True)


def get_num_solutions(
    design: str, patterns: list[str], cache: dict[str, int]
) -> None:
    """
    Updates the cache the number of possible combinations to create the
    given design
    """
    if cache.get(design) is None:
        cache[design] = 0
        for pattern in patterns:
            if design.startswith(pattern):
                cache[design] += get_num_solutions(
                    design.removeprefix(pattern), patterns, cache
                )
    return cache[design]


def find_solutions(designs: list[str], patterns: list[str]) -> int:
    """
    Returns total number of possible designs and the number of combinations to
    create the designs with the given patterns
    """
    cache = {'': 1}
    for design in designs:
        get_num_solutions(design, patterns, cache)

    possible_solutions = sum([1 for design in designs if cache[design] > 0])
    num_combinations = sum([cache[design] for design in designs])
    return possible_solutions, num_combinations


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    designs = extract_data_to_list(19)
    patterns = get_available_patterns(designs)
    return find_solutions(designs, patterns)
