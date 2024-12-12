from utils.utils import extract_data_to_list_of_list

Point = tuple[int, int]
Points = list[Point]
Grid = list[list[str]]
AntennaMap = dict[str, list[Point]]


def calculate_distance(point_1: Point, point_2: Point) -> Point:
    """
    Returns the row difference and column difference between point 2 and
    point 1
    """
    return point_2[0] - point_1[0], point_2[1] - point_1[1]


def get_possible_antinode(point: Point, slope: Point, sign: int) -> Point:
    """Returns a new point (either left or right of point depending on sign)"""
    row, col = point
    row_diff, col_diff = slope
    return row + sign * row_diff, col + sign * col_diff


def add_slope(point: Point, slope: Point) -> Point:
    """Adds the slope from the point"""
    return get_possible_antinode(point, slope, 1)


def subtract_slope(point: Point, slope: Point) -> Point:
    """Subtracts the slope from the point"""
    return get_possible_antinode(point, slope, -1)


def is_on_grid(grid: Grid, point: set[Point]) -> None:
    """Returns true if point is on the grid"""
    row_max, col_max = len(grid), len(grid[0])
    row, col = point
    return 0 <= row < row_max and 0 <= col < col_max


def find_antenna_antinodes(
    center: Point, points: Points, grid: Grid,
    antinodes: set[Point], harmonic_antinodes: set[Point]
) -> None:
    """Finds the potential antinodes on the grid based on two points"""
    for point in points:
        if center != point:
            slope = calculate_distance(center, point)
            left_side = subtract_slope(center, slope)
            if is_on_grid(grid, left_side):
                antinodes.add(left_side)
            harmonic_antinodes.add(center)
            while is_on_grid(grid, left_side):
                harmonic_antinodes.add(left_side)
                left_side = subtract_slope(left_side, slope)

            right_side = add_slope(point, slope)
            if is_on_grid(grid, right_side):
                antinodes.add(right_side)
            harmonic_antinodes.add(point)
            while is_on_grid(grid, right_side):
                harmonic_antinodes.add(right_side)
                right_side = add_slope(right_side, slope)


def find_all_antinodes(grid: Grid, antenna_map: AntennaMap) -> int:
    """Finds all colinear lines for each antenna"""
    antinodes = set()
    harmonic_antinodes = set()
    for antenna, locations in antenna_map.items():
        for point in locations:
            find_antenna_antinodes(
                point, locations, grid, antinodes, harmonic_antinodes
            )
    for row, col in harmonic_antinodes:
        grid[row][col] = '#'

    return len(antinodes), len(harmonic_antinodes)


def get_antenna_map(grid: Grid) -> AntennaMap:
    """
    Returns a dictionary with each type of antenna as a key and
    their locations stored in a list as tuples
    """
    antenna_map = {}
    for row, chars in enumerate(grid):
        for col, char in enumerate(chars):
            if char != '.':
                antenna_map.setdefault(char, []).append((row, col))
    return antenna_map


def print_grid(grid):
    for row in grid:
        for char in row:
            print(f'{char}', end="")
        print()


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    grid: Grid = extract_data_to_list_of_list(8)
    antenna_map: AntennaMap = get_antenna_map(grid)
    sol_1, sol_2 = find_all_antinodes(grid, antenna_map)
    print_grid(grid)

    return sol_1, sol_2
