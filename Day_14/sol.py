from utils.utils import extract_data_to_list

Point = tuple[int, int]
Grid = list[list[str | int]]


def get_start(data: str) -> Point:
    """Returns the starting point from the given data string"""
    points = data.split("p=")[1]
    points = points.split(",")
    x = points[0]
    y = points[1].split(" ")[0]

    return int(x), int(y)


def get_slope(data: str) -> Point:
    """Returns the slope in the form of rise over run (i.e., x,y)"""
    points = data.split("v=")[1]
    x_change, y_change = points.split(",")
    return int(x_change), int(y_change)


def solver(initial: Point, slope: Point, time: int) -> Point:
    """Returns the next point after the given change in time"""
    x_o, y_o = initial
    x_d, y_d = slope

    return (x_o + x_d * time), (y_o + y_d * time)


def grid_position(grid: Grid, point: Point) -> Point:
    """Returns the position on the grid"""
    y_len = len(grid)
    x_len = len(grid[0])
    x, y = point
    col = x % x_len if abs(x) >= x_len else x
    row = y % y_len if abs(y) >= y_len else y
    return row, col


def get_positions(data: list[str], grid: Grid, time: int = 100) -> list[Point]:
    """Gets the positions of the robots after time"""
    positions = []
    for line in data:
        initial = get_start(line)
        slope = get_slope(line)
        abs_position = solver(initial, slope, time)
        rel_position = grid_position(grid, abs_position)
        positions.append(rel_position)
    return positions


def create_grid(height: int, width: int, default_char: str = ".") -> Grid:
    """Returns a grid with the given height and width"""
    return [[default_char for _ in range(width)] for _ in range(height)]


def update_grid(robot_positions: list[Point], grid: Grid) -> None:
    """Updates the grid with the number of robots at each position"""
    for row, col in robot_positions:
        if not isinstance(grid[row][col], str):
            grid[row][col] = grid[row][col] + 1
        else:
            grid[row][col] = 1


def get_max_seq(grid: Grid) -> int:
    max_repeats = 0
    curr_repeats = 0
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            if val == " ":
                curr_repeats = 0
            else:
                curr_repeats += 1

            if curr_repeats > max_repeats:
                max_repeats = curr_repeats
    return max_repeats


def find_easter_egg(data: list[str]) -> int:
    """Displays the grid each iteration"""
    frames = {}
    for time in range(10000):
        grid = create_grid(103, 101, default_char=" ")
        new_positions = get_positions(data, grid, time)
        update_grid(new_positions, grid)
        frames[time] = get_max_seq(grid)

    times = sorted(frames.keys(), key=lambda time: frames[time], reverse=True)
    return times[0]


def get_score(grid: Grid) -> int:
    """Returns the score"""
    mid_row = int(len(grid)/2)
    mid_col = int(len(grid[0])/2)
    quads = [0, 0, 0, 0]
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            if val == '.':
                continue
            elif row < mid_row:
                if col < mid_col:
                    quads[0] += val
                elif col > mid_col:
                    quads[1] += val
            elif row > mid_row:
                if col < mid_col:
                    quads[2] += val
                elif col > mid_col:
                    quads[3] += val

    return quads[0] * quads[1] * quads[2] * quads[3]


def print_grid(grid: Grid) -> None:
    """Prints the grid"""
    for row in grid:
        for char in row:
            print(char, end="")
        print()


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    data = extract_data_to_list(14)
    grid = create_grid(103, 101)
    update_grid(get_positions(data, grid), grid)
    sol_1 = get_score(grid)
    sol_2 = find_easter_egg(data)

    return sol_1, sol_2
