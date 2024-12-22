from utils.utils import extract_data_to_list

Grid = list[list[str]]
Point = tuple[int, int]
Cheat = tuple[Point, Point, Point]


def print_grid(grid: Grid, pos: Point = (-1, -1)) -> None:
    """Prints the grid"""
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            print('o', end='') if (row, col) == pos else print(val, end='')
        print()
    return


def create_grid(data: list[str]) -> Grid:
    """Returns a grid from the data"""
    return [[val for val in row] for row in data]


def find_start(grid: Grid) -> Point:
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            if val == 'S':
                return row, col


def get_val(grid: Grid, point: Point) -> str:
    """Returns the value at the point"""
    row, col = point
    return grid[row][col]


def add_points(point_1: Point, point_2: Point) -> Point:
    """Return the addition of the two given tuples"""
    r_1, c_1 = point_1
    r_2, c_2 = point_2
    return r_1 + r_2, c_1 + c_2


def is_in_bounds(grid: Grid, point: Point) -> bool:
    """Returns true if point is on the grid"""
    row, col = point
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def get_all_neighbors(grid: Grid, point: Point) -> list[Point]:
    """Return a list of all neighbors"""
    neighbors = []
    for move in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        neighbor = add_points(point, move)
        if is_in_bounds(grid, neighbor):
            neighbors.append(add_points(point, move))
    return neighbors


def get_jumps(grid: Grid, point: Point) -> list[Cheat]:
    """Returns all cheats from a particular point"""
    neighbors = get_all_neighbors(grid, point)
    cheats = []
    for neighbor in neighbors:
        if get_val(grid, neighbor) == '#':
            jumps = get_all_neighbors(grid, neighbor)
            for jump in jumps:
                if jump != point and get_val(grid, jump) != '#':
                    cheats.append((point, neighbor, jump))
    return cheats


def get_all_cheats(grid: Grid, path: dict[Point, int]) -> set(Cheat):
    """Returns all the available cheats"""
    cheats = []
    for point in path.keys():
        cheats.extend(get_jumps(grid, point))
    return set(cheats)


def get_next_valid_move(
    grid: Grid, point: Point, visited: dict[Point, int]
) -> Point:
    """Return next valid move"""
    neighbors = get_all_neighbors(grid, point)
    for neighbor in neighbors:
        if visited.get(neighbor) or get_val(grid, neighbor) == '#':
            continue
        return neighbor


def expanded_cheats(
    grid: Grid, point: Point
) -> list[tuple[Point, Point, int]]:
    """Return a list of accessible points that within 20 moves"""
    row, col = point
    cheats = {}
    for row_diff in range(-20, 21):
        for col_diff in range(-20, 21):
            distance = abs(row_diff) + abs(col_diff)
            if distance > 20:
                continue
            target = add_points(point, (row_diff, col_diff))
            if is_in_bounds(grid, target) and get_val(grid, target) != '#':
                cheats[(point, target)] = min(
                    distance, cheats.get((point, target), 21)
                )
    unique_cheats = []
    for cheat, distance in cheats.items():
        start, target = cheat
        unique_cheats.append((start, target, distance))
    return unique_cheats


def find_path(grid: Grid, curr_pos: Point) -> list[Point]:
    """Finds the path and saves the distance from the end at each point"""
    path = [curr_pos]
    visited = {curr_pos: True}
    if visited is None:
        visited[curr_pos] = True
    next_pos = get_next_valid_move(grid, curr_pos, visited)

    while get_val(grid, curr_pos) != 'E':
        curr_pos = next_pos
        visited[curr_pos] = True
        path.append(curr_pos)
        next_pos = get_next_valid_move(grid, curr_pos, visited)
    return path


def get_pos_values(grid: Grid) -> dict[Point, int]:
    """
    Returns a dictionary with each point on the path and its distance to
    E
    """
    start = find_start(grid)
    path = find_path(grid, start)
    return dict(zip(path, range(len(path) - 1, -1, -1)))


def solution_1(grid: Grid) -> int:
    """Returns solution 1"""
    sol = {}
    pos_vals = get_pos_values(grid)
    cheats = get_all_cheats(grid, pos_vals)
    for start, wall, end in cheats:
        time_saved = pos_vals[start] - pos_vals[end] - 2
        if time_saved > 0:
            sol[time_saved] = sol.get(time_saved, 0) + 1
    return sum([freq for time_saved, freq in sol.items() if time_saved >= 100])


def solution_2(grid: Grid) -> int:
    """Returns solution 2"""
    sol = {}
    pos_vals = get_pos_values(grid)
    cheats = []
    for point in pos_vals.keys():
        cheats.extend(expanded_cheats(grid, point))
    unique_cheats = set(cheats)

    for start, end, distance in unique_cheats:
        time_saved = pos_vals[start] - pos_vals[end] - distance
        if time_saved > 0:
            sol[time_saved] = sol.get(time_saved, 0) + 1
    return sum([freq for time_saved, freq in sol.items() if time_saved >= 100])


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    grid = create_grid(extract_data_to_list(20))
    sol_1 = solution_1(grid)
    sol_2 = solution_2(grid)

    return sol_1, sol_2
