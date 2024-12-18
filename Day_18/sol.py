from utils.utils import extract_data_to_list

Grid = list[list[str]]
Point = tuple[int, int]
Points = list[Point]


def print_grid_snippet(
    grid: Grid, pos: Point, neighbors: Points, queue: list[Points]
) -> None:
    """Prints a small snippet of the grid"""
    queued = [point for sublist in queue for point in sublist]
    r, c = pos
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            if r-10 < row < r+10 and c-10 < col < c+10:
                if (row, col) == pos:
                    print('o', end='')
                elif (row, col) in neighbors:
                    print('n', end='')
                elif (row, col) in queued:
                    print('q', end='')
                else:
                    print(val, end='')
        if r-10 < row < r+10:
            print()
    return


def print_grid(grid: Grid, pos: Point = (-1, -1)) -> None:
    """Prints the grid"""
    for row, vals in enumerate(grid):
        for col, val in enumerate(vals):
            print('o', end='') if (row, col) == pos else print(val, end='')
        print()
    return


def create_grid(data: list[str], width: int, height: int, limit: int) -> Grid:
    """Returns a grid with obstacles"""
    points = [tuple([int(num) for num in line.split(',')]) for line in data]
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for col, row in points[:limit]:
        grid[row][col] = '#'
    return grid


def get_val(grid: Grid, point: Point) -> str:
    """Returns the value of grid at point"""
    row, col = point
    return grid[row][col]


def is_in_bounds(grid: Grid, point: Point) -> bool:
    """Returns true if point is within grid limits"""
    row, col = point
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def add_point(point: Point, change: Point) -> Point:
    """Returns point + change"""
    row, col = point
    row_delta, col_delta = change
    return row + row_delta, col + col_delta


def get_distance(grid: Grid, point: Point, end: Point) -> int:
    row, col = point
    tar_row, tar_col = end
    return abs(row - tar_row) + abs(col - tar_col)


def get_options(
    grid: Grid, point: Point, visited: dict[Point, int], score: int, end: Point
) -> Points:
    """
    Return available options from the point. Point must be available,
    and unvisited or cost less to visit from current path
    """
    points = []
    for delta in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        option = add_point(point, delta)
        if is_in_bounds(grid, option) and get_val(grid, option) == '.':
            if visited.get(option) is None or score < visited.get(option):
                visited[option] = score
                points.append(option)
    return sorted(points, key=lambda point: get_distance(grid, point, end))


def bfs(grid: Grid, start: Point, end: Point) -> int | None:
    """
    Searches for a path from start to end using bfs. Returns None if
    end cannot be found from start
    """
    curr_pos = start
    score = 0
    visited = {start: score}

    score += 1
    queue = [get_options(grid, curr_pos, visited, score, end)]
    neighbors = queue.pop()
    cache = []
    while curr_pos != end:
        if len(neighbors) > 0:
            curr_pos = neighbors.pop()
            cache.append(curr_pos)
        elif len(queue) > 0:
            neighbors = queue.pop(0)
        elif len(cache) > 0:
            score += 1
            for point in cache:
                queue.append(get_options(grid, point, visited, score, end))
            cache.clear()
        else:
            score = None
            break
    return score


def find_blocking_byte() -> str:
    """Finds the byte that prevents a solutions from being found"""
    data = extract_data_to_list(18)
    for i in range(1024, len(data)):
        grid = create_grid(data, 71, 71, i)
        score = bfs(grid, (0, 0), (70, 70))
        if score is None:
            return data[i-1]


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    grid = create_grid(extract_data_to_list(18), 71, 71, 1024)
    sol_1 = bfs(grid, (0, 0), (70, 70))
    sol_2 = find_blocking_byte()
    return sol_1, sol_2
