from utils.utils import extract_data_to_list

Grid = list[list[str]]
Point = tuple[int, int]
Line = tuple[int, int]


def separate_grid_and_moves(data: list[str]) -> tuple[Grid, str]:
    """Separates the input data into a grid and a string of moves"""
    grid = []
    for line in data:
        if line == '':
            break
        grid.append(list(line))
    moves = ""
    capture = False
    for line in data:
        capture = True if line == '' else capture
        if capture:
            moves += line
    return grid, moves


def find_start(grid: Grid) -> Point:
    """Finds the @ in the grid"""
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            if val == '@':
                return row, col


def get_val(grid: Grid, point: Point) -> str:
    """Returns the value at the point in the grid"""
    row, col = point
    return grid[row][col]


def swap_vals(grid: Grid, point_1: Point, point_2: Point) -> None:
    """Swaps the values at point_1 and point_2"""
    r_1, c_1 = point_1
    r_2, c_2 = point_2
    grid[r_1][c_1], grid[r_2][c_2] = grid[r_2][c_2], grid[r_1][c_1]


def get_move(move: str) -> Point:
    """Returns the move in row, col format based on string"""
    moves = {'^': (-1, 0), '<': (0, -1), '>': (0, 1), 'v': (1, 0)}
    return moves[move]


def shift_point(point: Point, move: Point) -> Point:
    """
    Returns the new point that results from
    moving point in the given direction
    """
    row, col = point
    row_change, col_change = move
    return row + row_change, col + col_change


def shift_boxes(grid: Grid, curr_pos: Point, move: Point) -> None:
    """Moves point and boxes to next available position"""
    next_pos = shift_point(curr_pos, move)
    next_pos_val = get_val(grid, next_pos)

    if next_pos_val == '.':
        swap_vals(grid, curr_pos, next_pos)
        return next_pos
    elif next_pos_val == 'O':
        shift_boxes(grid, next_pos, move)
        if get_val(grid, next_pos) == '.':
            swap_vals(grid, curr_pos, next_pos)
            return next_pos
    return curr_pos


def follow_moves(grid: Grid, moves: str) -> None:
    """Follows the moves on the grid"""
    pos = find_start(grid)
    for move in moves:
        act_move = get_move(move)
        pos = shift_boxes(grid, pos, act_move)
    return


def get_gps(point: Point) -> int:
    """Returns the GPS of the point"""
    row, col = point
    return 100*row+col


def get_gps_sum(grid: Grid) -> int:
    """Returns the total gps of all boxes"""
    total = 0
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            if val == 'O' or val == '[':
                total += get_gps((row, col))
    return total


def print_grid(grid: Grid):
    """Print the grid"""
    for row in grid:
        for char in row:
            print(char, end="")
        print()
    return


def double_grid(grid: Grid) -> Grid:
    """Double the grid"""
    new_grid = []
    for row in grid:
        new_row = []
        for val in row:
            if val == '#':
                new_row.extend(['#', '#'])
            elif val == '@':
                new_row.extend(['@', '.'])
            elif val == 'O':
                new_row.extend(['[', ']'])
            else:
                new_row.extend(['.', '.'])
        new_grid.append(new_row)
    return new_grid


def shift_box_horizontal(grid: Grid, row: int, start: int, end: int) -> None:
    """
    Continues to shift boxes horizontally until the
    free space is the start
    """

    direction = 1 if end < start else -1
    col = end

    while col != start:
        next_col = col + direction
        grid[row][col], grid[row][next_col] = (
            grid[row][next_col], grid[row][col]
        )
        col = next_col
    return


def find_horizontal_free_space(grid: Grid, pos: Point, direction: str) -> int:
    """Returns the next available free space or -1 if not found"""
    row, col = pos
    direction = -1 if direction == '<' else 1

    # Keep incrementing col until '[' or ']' is not in the space
    col += direction
    while get_val(grid, (row, col)) in ['[', ']']:
        col += direction

    # If a free space is found at row, col, return the col value
    if get_val(grid, (row, col)) == '.':
        return col
    return -1


def check_space_above(grid: Grid, row: int, col: int, direction: int) -> bool:
    """Check if vertical movement is clear"""
    next_row = row + direction
    curr_val = get_val(grid, (row, col))
    next_val = get_val(grid, (next_row, col))

    availability = []
    if next_val == '[' and curr_val != next_val:
        availability.append(check_space_above(grid, next_row, col, direction))
        availability.append(
            check_space_above(grid, next_row, col+1, direction)
        )
    elif next_val == ']' and curr_val != next_val:
        availability.append(check_space_above(grid, next_row, col, direction))
        availability.append(
            check_space_above(grid, next_row, col-1, direction)
        )
    elif next_val == curr_val:
        availability.append(check_space_above(grid, next_row, col, direction))
    elif next_val == '#':
        availability.append(False)
    else:
        availability.append(True)
    for val in availability:
        if not val:
            return False
    return True


def shift_up(grid: Grid, row: int, col: int, direction: int) -> None:
    """Shift spaces vertically"""
    next_row = row + direction
    curr_val = get_val(grid, (row, col))
    next_val = get_val(grid, (next_row, col))

    if next_val == '[' and curr_val != next_val:
        shift_up(grid, next_row, col, direction)
        shift_up(grid, next_row, col+1, direction)

    elif next_val == ']' and curr_val != next_val:
        shift_up(grid, next_row, col, direction)
        shift_up(grid, next_row, col-1, direction)

    elif next_val == curr_val:
        shift_up(grid, next_row, col, direction)

    grid[row][col], grid[next_row][col] = (
        grid[next_row][col], grid[row][col]
    )


def do_double_move(grid: Grid, curr_pos: Point, move: str):
    row, col = curr_pos
    if move == '<' or move == '>':
        next_free_space = find_horizontal_free_space(grid, curr_pos, move)
        if next_free_space > 0:
            shift_box_horizontal(grid, row, col, next_free_space)
    elif move == 'v':
        if check_space_above(grid, row, col, direction=1):
            shift_up(grid, row, col, direction=1)
    else:
        if check_space_above(grid, row, col, direction=-1):
            shift_up(grid, row, col, direction=-1)
    return


def follow_moves_on_double_map(grid: Grid, moves: str) -> None:
    pos = find_start(grid)
    for move in moves:
        do_double_move(grid, pos, move)
        pos = find_start(grid)
    print_grid(grid)


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    data = extract_data_to_list(15)
    grid, moves = separate_grid_and_moves(data)
    follow_moves(grid, moves)
    sol_1 = get_gps_sum(grid)

    data = extract_data_to_list(15)
    grid, moves = separate_grid_and_moves(data)
    new_grid = double_grid(grid)
    follow_moves_on_double_map(new_grid, moves)
    sol_2 = get_gps_sum(new_grid)

    return sol_1, sol_2
