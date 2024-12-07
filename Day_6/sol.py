from utils.utils import extract_data_to_list
from typing import Callable


def direction_gen() -> tuple[int, int]:
    """Yields the next direction tuple"""
    while True:
        for i, j in zip([-1, 0, 1, 0], [0, 1, 0, -1]):
            yield (i, j)


def get_next_direction() -> Callable[[], [tuple[int, int]]]:
    """Yields the next direction tuple"""
    next_direction = direction_gen()
    return lambda: next(next_direction)


def convert_rows_to_string(data: list[str]) -> None:
    """Converts each row in data to a list"""
    for idx in range(len(data)):
        data[idx] = list(data[idx])
    return


def find_start(data: list[list[str]]) -> tuple[int, int]:
    """Finds the position of the ^ in the data"""
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == '^':
                return row, col


def get_next_pos(
    current_pos: tuple[int, int], direction: tuple[int, int]
) -> tuple[int, int]:
    """Returns the next position with the given direction"""
    return [curr+change for curr, change in zip(current_pos, direction)]


def in_bounds(data: list[list[str]], current_pos: tuple[int, int]) -> bool:
    """Returns True of the current position is in bounds"""
    return (
        0 <= current_pos[0] < len(data)
        and 0 <= current_pos[1] < len(data[current_pos[0]])
    )


def move_on_map(data: list[list[str]], start_pos: tuple[int, int]) -> int:
    """Returns the number of locations visited while moving on map"""
    turn = get_next_direction()
    direction = turn()
    seen = set()
    seen.add(tuple(start_pos))
    pos = get_next_pos(start_pos, direction)
    next_pos = pos
    while in_bounds(data, next_pos):
        if data[next_pos[0]][next_pos[1]] == '#':
            direction = turn()
        else:
            pos = next_pos
            seen.add(tuple(pos))
        next_pos = get_next_pos(pos, direction)
    return len(seen)


def get_reset_direction_gen(
    reset_val: tuple[int, int] = (-1, 0)
) -> Callable[[], [tuple[int, int]]]:
    """Returns the direction generator that is reset to (-1, 0)"""
    turn = get_next_direction()
    direction = turn()
    while direction != reset_val:
        direction = turn()
    return turn


def is_infinite_loop(data: list[list[str]], start: tuple[int, int]) -> bool:
    """Returns true if data is in an infinite loop"""
    # Get the direction
    turn = get_reset_direction_gen()
    direction = (-1, 0)

    # Create a set of seen points
    seen = set()
    seen.add(tuple(start)+direction)

    pos = start
    next_pos = get_next_pos(start, direction)
    while in_bounds(data, next_pos):
        if data[next_pos[0]][next_pos[1]] == '#':
            direction = turn()
        else:
            pos = next_pos
            # data[next_pos[0]][next_pos[1]] = 's'
            pos_and_dir = tuple(pos) + direction
            if pos_and_dir in seen:
                return True
            else:
                seen.add(pos_and_dir)
        next_pos = get_next_pos(pos, direction)
    return False


def num_infinite_loops(data: list[list[str]], start: tuple[int, int]) -> int:
    """
    Returns the number of possible infinite loops that can be created by
    placing obstacles in the path.
    """
    # Get the direction
    turn = get_reset_direction_gen()
    direction = (-1, 0)

    infinite_loops = set()
    pos = start
    next_pos = get_next_pos(start, direction)
    while in_bounds(data, next_pos):
        if data[next_pos[0]][next_pos[1]] != '#':
            data[next_pos[0]][next_pos[1]] = '#'
            if is_infinite_loop(data, start):
                infinite_loops.add(tuple(next_pos))
            # reset turn and map
            turn = get_reset_direction_gen(direction)
            data[next_pos[0]][next_pos[1]] = '.'

        if data[next_pos[0]][next_pos[1]] == '#':
            direction = turn()
        else:
            pos = next_pos
        next_pos = get_next_pos(pos, direction)
    return len(infinite_loops)



def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    data = extract_data_to_list(6)
    convert_rows_to_string(data)
    start = find_start(data)
    sol_1 = move_on_map(data, start)
    sol_2 = num_infinite_loops(data, start)
    return sol_1, sol_2
