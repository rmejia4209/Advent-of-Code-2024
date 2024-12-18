from utils.utils import extract_data_to_list

Grid = list[list[str]]
Point = tuple[int, int]
Points = list[tuple[Point, str]]


def convert_to_grid(data: list[str]) -> Grid:
    """Returns a grid from the input data"""
    return [list(row) for row in data]


def find_start(grid: Grid) -> Point:
    """Find the start"""
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            if val == 'S':
                return row, col


def print_grid(grid: Grid) -> None:
    """Prints the grid"""
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            print(val, end='')
        print()
    return


def print_small_window(grid: Grid, point: Point) -> None:
    r, c = point
    for row, vals in enumerate(grid):
        if r-4 < row < r+5:
            print(f'{row} ', end='')
        for col, val in enumerate(vals):
            if r-4 < row < r+5 and c-4 < col < c+5:
                if row == r and col == c:
                    print('O', end='')
                else:
                    print(val, end='')
        print()


def print_current_location(
    grid: Grid, location: Point, dir: str, path: Points
) -> None:
    """Prints the grid with a cursor at the location"""
    chars = {'N': '^', 'E': '>', 'S': 'v', 'W': '<'}
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            if (row, col) == location:
                print(chars[dir], end='')
            elif (row, col) in path:
                print('o', end='')
            else:
                print(val, end='')
        print()
    return


def get_val(grid: Grid, point: Point) -> str:
    """Returns the value on the grid at the given point"""
    row, col = point
    return grid[row][col]


def set_val(grid: Grid, point: Point, direction: str) -> None:
    """Sets the value at the point based on the direction"""
    row, col = point
    chars = {'N': '^', 'E': '>', 'S': 'v', 'W': '<'}
    grid[row][col] = chars[direction]
    return


def get_next_point(point: Point, movement: str) -> Point:
    """Returns the next point given the movement"""
    movement_dict = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    row_change, col_change = movement_dict[movement]
    row, col = point
    return row + row_change, col + col_change


def get_options(grid: Grid, position: Point, last_pos: Point) -> Points:
    """Return possible options from the given position"""
    options = []
    for move in ['N', 'S', 'W', 'E']:
        next_point = get_next_point(position, move)
        next_val = get_val(grid, next_point)
        if next_val != '#' and next_point != last_pos:
            options.append((next_point, move))
    return options


def rotate(current_direction: str, target_direction: str) -> int:
    """Returns the penalty associated with rotating to the target direction"""
    penalty_map = {
        'N': ['E', 'W'], 'S': ['E', 'W'], 'E': ['N', 'S'], 'W': ['N', 'S']
    }
    if target_direction in penalty_map[current_direction]:
        return 1000
    return 2000


def is_viable_path(
    visited: dict[tuple[int, int], Points], point: Point, score: int
) -> bool:
    """
    Returns true if given score is a minimum or point has not been visited.
    Updates the visited dict
    """

    if visited.get(point):
        if score > (visited.get(point)+1000):
            return False
        else:
            visited[point] = score
    else:
        visited[point] = score
    return True


def update_score(score: int, curr_dir: str, next_dir: str) -> int:
    """Updates the score"""
    score += rotate(curr_dir, next_dir) if curr_dir != next_dir else 0
    return score + 1


def solve_maze(
    grid: Grid, position: Point, curr_dir: str, score: int, scores: list[int],
    paths: dict[int, list[Points]], visited: dict[tuple[int, int], int] = None,
    last_pos: Point = None, current_path: Points = None
) -> int:
    """TODO"""

    if visited is None:
        visited = {}
    if last_pos is None:
        last_pos = position
    if current_path is None:
        current_path = []

    moves = get_options(grid, position, last_pos)
    while len(moves) == 1:
        next_pos, next_dir = moves[0]
        new_score = update_score(score, curr_dir, next_dir)
        if not is_viable_path(visited, next_pos, new_score):
            moves.clear()
        elif get_val(grid, next_pos) == 'E':
            scores.append(new_score)
            current_path.append(position)
            paths.setdefault(new_score, []).append(current_path[:])
            moves.clear()
        else:
            current_path.append(position)
            score = new_score
            last_pos = position
            position = next_pos
            curr_dir = next_dir
            moves = get_options(grid, position, last_pos)

    for next_pos, next_dir in moves:
        new_score = update_score(score, curr_dir, next_dir)
        if len(scores) > 0 and new_score > min(scores):
            break
        elif get_val(grid, next_pos) == 'E':
            scores.append(new_score)
            current_path.append(position)
            paths.setdefault(new_score, []).append(current_path)
        elif is_viable_path(visited, next_pos, new_score):
            current_path.append(position)
            solve_maze(
                grid, next_pos, next_dir, new_score, scores, paths,
                visited, position, current_path[:]
            )
    return scores


def get_paths(grid: Grid) -> int:
    """Returns the best paths dict"""
    start = find_start(grid)
    scores = []
    paths = {}
    solve_maze(
        grid, start, curr_dir='E', score=0, scores=scores, paths=paths
        )
    return paths


def mark_best_seats(grid: Grid, paths: dict[int, list[Points]]) -> None:
    """Marks the best seats on the grid"""
    min_val = min(paths.keys())
    print(len(paths[min_val]))
    for path in paths[min_val]:
        for row, col in path:
            grid[row][col] = 'O'
    return


def count_best_seats(grid: Grid) -> int:
    """Counts the number of best seats"""
    total = 0
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            if val != '.' and val != '#':
                total += 1
    return total


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    grid = convert_to_grid(extract_data_to_list(16))
    paths = get_paths(grid)
    mark_best_seats(grid, paths)
    sol_1 = min(paths.keys())
    print_grid(grid)
    sol_2 = count_best_seats(grid)
    return sol_1, sol_2
