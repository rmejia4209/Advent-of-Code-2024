from utils.utils import extract_data_to_list_of_list

Grid = list[list[str]]
Point = tuple[int, int]
Hash = dict[str, int]


def is_diff(grid: Grid, point: Point, neighbor: Point) -> bool:
    """Returns true if the plots at point and neighbor are the different"""
    row, col = point
    neighbor_row, neighbor_col = neighbor
    return grid[row][col] != grid[neighbor_row][neighbor_col]


def is_out_of_bounds(grid: Grid, point: Point) -> bool:
    """Returns true if the point is out of bounds"""
    row_max, col_max = len(grid), len(grid[0])
    row, col = point
    return not (0 <= row < row_max and 0 <= col < col_max)


def is_outside_corner(
    grid: Grid, corner: Point, point_1: Point, point_2: Point
) -> bool:
    """Return's true if point is a corner with respect to points 1 and 2"""

    return (
        (is_out_of_bounds(grid, point_1) or is_diff(grid, corner, point_1))
        and
        (is_out_of_bounds(grid, point_2) or is_diff(grid, corner, point_2))
    )


def is_inside_corner(
    grid: Grid, corner: Point, point_1: Point, point_2: Point
) -> bool:
    """
    Returns True if corner, point_1, point_2 form
    a Match, Different, Match pattern
    """
    # Inside corners cannot occur on boundaries
    if is_out_of_bounds(grid, point_1) or is_out_of_bounds(grid, point_2):
        return False
    if is_diff(grid, corner, point_1) and not is_diff(grid, corner, point_2):
        return True
    return False


def get_num_corners(grid: Grid, corner: Point) -> int:
    """Returns the number of corners at a point"""
    row, col = corner
    corners = 0
    for _, hor_diff in [(0, -1), (0, 1)]:
        for vert_diff, _ in [(-1, 0), (1, 0)]:
            point_1 = row, col + hor_diff
            point_2 = row + vert_diff, col
            point_3 = point_1[0] + vert_diff, point_1[1]
            if is_outside_corner(grid, corner, point_1, point_2):
                corners += 1
            elif is_inside_corner(grid, corner, point_1, point_3):
                corners += 1
    return corners


def get_adjacent_plots(point: Point) -> list[Point]:
    """
    Returns the points to the left, right, above, and below the given point
    """
    neighbors = []
    row, col = point
    for row_diff, col_diff in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        neighbor = (row+row_diff, col+col_diff)
        neighbors.append(neighbor)
    return neighbors


def get_perimeter_per_point(grid: Grid, point: Point) -> int:
    """
    Finds the number of sides that are on the boundary of the grid
    or contain a plot that does not match the grid
    """
    neighbors = get_adjacent_plots(point)
    perimeter = 0
    for neighbor in neighbors:
        if is_out_of_bounds(grid, neighbor) or is_diff(grid, point, neighbor):
            perimeter += 1
    return perimeter


def gen_unvisited_plot_list(grid: Grid) -> list[Point]:
    """Returns all of the plot points as a list"""
    return [
        (row, col) for row in range(len(grid)) for col in range(len(grid[0]))
    ]


def get_matching_adjacent_plots(
    grid: Grid, point: Point, visited: list[Point], queued: list[Point]
) -> list[Point]:
    """Returns a list of adjacent matching plots"""
    valid_neighbors = []
    for neighbor in get_adjacent_plots(point):
        if is_out_of_bounds(grid, neighbor) or is_diff(grid, point, neighbor):
            continue
        valid_neighbors.append(neighbor)

    visited.extend(queued)
    return [
        neighbor for neighbor in valid_neighbors if neighbor not in visited
    ]


def update_unvisited_plots(
    unvisited_plots: list[Point], queued_plots: list[Point]
) -> list[Point]:
    """
    Updates the unvisited_plot list by removed plots that have been queued
    """
    return [plot for plot in unvisited_plots if plot not in queued_plots]


def bfs(grid: Grid) -> dict[int, dict[str, int | str]]:
    """
    Finds all the regions in a grid and returns a dict with each regions
    plot type, area, and perimeter
    """
    unvisited = gen_unvisited_plot_list(grid)
    visited = []
    next_plot = unvisited.pop(0)

    queued_plots = get_matching_adjacent_plots(
        grid, next_plot, visited, [])
    unvisited = update_unvisited_plots(unvisited, queued_plots)

    region_id = 0
    plot_dict = {region_id: {}}
    while next_plot:
        # Update Region's area & perimeter
        row, col = next_plot
        plot_dict[region_id].setdefault('plot', grid[row][col])
        plot_dict[region_id]['area'] = plot_dict[region_id].get('area', 0) + 1
        plot_dict[region_id]['perimeter'] = (
            plot_dict[region_id].get('perimeter', 0)
            + get_perimeter_per_point(grid, (row, col))
        )
        plot_dict[region_id]['corners'] = (
            plot_dict[region_id].get('corners', 0)
            + get_num_corners(grid, (row, col))
        )
        # Update region if no neighboring plots are left
        visited.append(next_plot)
        if len(queued_plots) == 0:
            region_id += 1
            plot_dict.setdefault(region_id, {})
            next_plot = unvisited.pop(0) if len(unvisited) else None
        else:
            next_plot = queued_plots.pop(0)

        if next_plot:
            queued_plots.extend(
                get_matching_adjacent_plots(
                    grid, next_plot, visited, queued_plots
                )
            )
            unvisited = update_unvisited_plots(unvisited, queued_plots)
        print(len(unvisited))
    return plot_dict


def get_total_fencing_cost(plot_dict: dict[int, dict[str, int | str]]) -> int:
    """Return the total fencing cost"""
    return sum([
        plot['area'] * plot['perimeter'] for plot in plot_dict.values() if plot
    ])


def get_reduced_cost(plot_dict: dict[int, dict[str, int | str]]) -> int:
    """Return the total fencing cost"""
    return sum([
        plot['area'] * plot['corners'] for plot in plot_dict.values() if plot
    ])


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    grid: Grid = extract_data_to_list_of_list(12)
    plot_dict = bfs(grid)
    for plot in plot_dict.values():
        print(plot)
    sol_1 = get_total_fencing_cost(plot_dict)
    sol_2 = get_reduced_cost(plot_dict)

    return sol_1, sol_2
