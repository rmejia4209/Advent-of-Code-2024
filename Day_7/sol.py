from utils.utils import extract_data_to_list


def create_operation_permutations(
    target_len: int, *,
    unique_combos: set[tuple[str, ...]] | None = None,
    current_ops: list[str] | None = None,
    valid_operators: list[str] | None = None
) -> set[tuple[str, ...]]:
    """
    Returns a set of all of the possible combinations of + * operations
    possible with the target length
    """

    unique_combos = set() if unique_combos is None else unique_combos
    current_ops = [] if current_ops is None else current_ops
    valid_operators = ['+', '*'] if not valid_operators else valid_operators

    if len(current_ops) < target_len:
        for operator in valid_operators:
            appended_ops = current_ops[:]
            appended_ops.append(operator)
            create_operation_permutations(
                target_len,
                unique_combos=unique_combos,
                current_ops=appended_ops,
                valid_operators=valid_operators
            )
    else:
        unique_combos.add(tuple(current_ops))
    return unique_combos


def perform_operations(nums: list[int], operations: tuple[str, ...]) -> int:
    """
    Returns the total results from performing the operation in operations 
    left to right on nums
    """

    total = nums[0]
    operations = list(operations)
    for num in nums[1:]:
        operation = operations.pop(0)
        if operation == '+':
            total += num
        elif operation == '*':
            total *= num
        else:
            left_hand = str(total)
            right_hand = str(num)
            total = int(left_hand+right_hand)
    return total


def has_solution(target: int, nums: list[int], concat: bool = False) -> bool:
    """
    Returns True if there is a combination of '+' and '*' that
    can be performed on nums to result in the target solution
    """
    valid_operators = ['+', '*', '||'] if concat else ['+', '*']
    possible_operations = create_operation_permutations(
        target_len=len(nums)-1,
        valid_operators=valid_operators
    )

    for operation in possible_operations:
        result = perform_operations(nums, operation)
        if result == target:
            return True
    return False


def find_valid_sums(data: list[tuple[int, list[int]]]) -> int:
    """Finds the sum of all of the valid equations in data"""
    total = 0
    for solution, nums in data:
        total += solution if has_solution(solution, nums) else 0
    return total


def find_valid_sums_2(data: list[tuple[int, list[int]]]) -> int:
    """Finds the sum of all of the valid equations in data with || included"""
    total = 0
    for solution, nums in data:
        total += solution if has_solution(solution, nums, concat=True) else 0
    return total


def convert_data(data: list[str]) -> list[tuple[int, list[int]]]:
    """
    Converts the data from a list of strings to a dictionary with
    the target solution as the key and the numbers as the value
    """
    new_data = []
    for row in data:
        components = row.split(": ")
        target = int(components[0])
        nums = [int(val) for val in components[1].split(" ")]
        new_data.append((target, nums))
    return new_data


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    data = extract_data_to_list(7)
    data = convert_data(data)
    sol_1 = find_valid_sums(data)
    sol_2 = find_valid_sums_2(data)
    return sol_1, sol_2
