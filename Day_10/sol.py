from utils.utils import extract_data_to_list_of_list

Grid = list[list[int]]
Point = tuple[int, int]


def convert_to_grid(data: list[list[str]]) -> Grid:
    """Returns a list of list of ints from a list of list of strings"""
    grid = []
    for row in data:
        grid.append([int(num) for num in row])
    return grid


def find_trail_heads(grid: Grid) -> list[Point]:
    """Return a list of all 0 positions in the data"""
    trail_heads = []
    for row, nums in enumerate(grid):
        for col, num in enumerate(nums):
            if num == 0:
                trail_heads.append((row, col))
    return trail_heads


def in_bounds(point: Point, grid: Grid) -> bool:
    """Returns true if the point is within the bounds of the grid"""
    row, col = point
    row_max, col_max = len(grid), len(grid[0])
    return 0 <= row < row_max and 0 <= col < col_max


def get_val(grid: Grid, point: Point) -> int:
    """Returns the value at the given point"""
    row, col = point
    return grid[row][col]


def get_available_moves(point: Point, cur_val: int, grid: Grid) -> list[Point]:
    """
    Returns a list of points that are one more than 
    the value at point on the grid
    """
    row, col = point
    tar_val = cur_val + 1
    available_moves = []
    for row_diff, col_diff in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        new_point = (row + row_diff, col + col_diff)
        if in_bounds(new_point, grid) and get_val(grid, new_point) == tar_val:
            available_moves.append(new_point)
    return available_moves


def next_move(grid: Grid, point: Point, end_points: list[Point]) -> None:
    """
    Recursively finds paths starting from the given point.
    Returns when no moves are available or the current value is 9
    """
    cur_val = get_val(grid, point)
    if cur_val == 9:
        end_points.append(point)
    else:
        moves = get_available_moves(point, cur_val, grid)
        for move in moves:
            next_move(grid, move, end_points)
    return


def find_paths(grid: Grid, trail_heads: list[Point]) -> tuple[int, int]:
    """Finds the score of each trail head"""
    end_points = []
    total_unique_trails = 0
    total_paths = 0
    for start in trail_heads:
        next_move(grid, start, end_points)
        total_unique_trails += len(set(end_points))
        total_paths += len(end_points)
        end_points.clear()
    return total_unique_trails, total_paths


def solution() -> tuple[int, int]:
    grid = convert_to_grid(extract_data_to_list_of_list(10))
    trail_heads = find_trail_heads(grid)
    sol_1, sol_2 = find_paths(grid, trail_heads)

    return sol_1, sol_2
