from utils.utils import extract_data_to_list


def get_rules(data: list[str]) -> dict[str, list[str]]:
    """Returns the rules (i.e., 74|43) from data"""
    rules = {}
    for row in data:
        if "|" in row:
            num_1, num_2 = row.split("|")
            rules.setdefault(num_1, []).append(num_2)
    return rules


def get_update_pages(data: list[str]) -> list[list[str]]:
    """Removes the rules from the data and returns a 2d list of strings"""
    new_data = []
    for row in data:
        if "|" not in row and len(row) > 0:
            new_data.append(row.split(","))
    return new_data


def is_valid(num: str, rules: dict[str, list[str]], pages: list[str]) -> bool:
    """Returns true if no page in pages is found in rules[num]"""
    for page in pages:
        if page in rules.get(num, []):
            return False
    return True


def separate_sequences(
    data: list[list[str]], rules: dict[str, list[str]]
) -> tuple[list[list[str]], list[list[str]]]:
    """Separates the valid sequences from invalid sequences"""
    valid = []
    invalid = []

    for manual in data:
        placed = False
        for idx, page in enumerate(manual):
            if not is_valid(page, rules, manual[:idx]):
                invalid.append(manual)
                placed = True
                break
        if not placed:
            valid.append(manual)
    return valid, invalid


def get_middle_page_sum(data: list[list[str]]) -> int:
    """Returns the sum of the middle index of each list"""
    sum_total = 0
    for manual in data:
        sum_total += int(manual[(int(len(manual)/2))])
    return sum_total


def fix_order(old_order: list[str], rules: dict[str, list[str]]) -> list[str]:
    """Fixes the order and returns the mid point to be summed"""
    new_order = []
    for page in old_order:
        append = True
        for idx in range(len(new_order)):
            if new_order[idx] in rules.get(page, []):
                new_order.insert(idx, page)
                append = False
                break
        if append:
            new_order.append(page)

    return int(new_order[(int(len(new_order)/2))])


def get_fixed_midpoints_sum(
    data: list[list[str]], rules: dict[str, list[str]]
) -> int:
    """Get the total sum of all the mid points of the corrected sequences"""
    total_sum = 0
    for row in data:
        midpoint = fix_order(row, rules)
        total_sum += midpoint
    return total_sum


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    data = extract_data_to_list(5)
    rules, data = get_rules(data), get_update_pages(data)
    valid, invalid = separate_sequences(data, rules)

    sol_1 = get_middle_page_sum(valid)
    sol_2 = get_fixed_midpoints_sum(invalid, rules)

    return sol_1, sol_2
