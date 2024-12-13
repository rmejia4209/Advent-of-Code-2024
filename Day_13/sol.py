import numpy as np
from utils.utils import extract_data_to_list

Matrix = tuple[list[list[int]], list[int]]


def create_data_chunks(data: list[str]) -> list[list[str]]:
    """Returns a list of list of problems"""
    data_chunks = []
    chunk = []
    for item in data:
        if item:
            chunk.append(item)
        else:
            data_chunks.append(chunk[:])
            chunk.clear()
    data_chunks.append(chunk)
    return data_chunks


def get_coefficients(data: str):
    """Returns the x and y coefficients from the given input"""
    words = data.split(": ")
    words = words[1].split(", ")
    x_coefficient = words[0].split("+")[1]
    y_coefficient = words[1].split("+")[1]
    return int(x_coefficient), int(y_coefficient)


def get_answers(data: str, modify: bool) -> tuple[int, int]:
    """Returns the x and y solutions from the given input"""
    words = data.split(": ")
    words = words[1].split(", ")
    x_ans = int(words[0].split("=")[1])
    y_ans = int(words[1].split("=")[1])

    if modify:
        x_ans += 10000000000000
        y_ans += 10000000000000

    return x_ans, y_ans


def create_matrix(data_chunk: list[str], modify: bool) -> Matrix:
    """Creates a Matrix based on the data chunk"""
    a_coefficients = get_coefficients(data_chunk[0])
    b_coefficients = get_coefficients(data_chunk[1])
    answers = get_answers(data_chunk[2], modify)

    coefficients = []
    for a, b, in zip(a_coefficients, b_coefficients):
        coefficients.append([a, b])
    return coefficients, answers


def create_matrices(
    data_chunks: list[list[str]], modify: bool = False
) -> list[Matrix]:
    """Converts each data chunk into a matrix"""
    matrices = []
    for chunk in data_chunks:
        matrices.append(create_matrix(chunk, modify))
    return matrices


def verify_solutions(solutions: tuple[float, float]) -> tuple[int, int]:
    """Verifies solutions are greater than 100"""
    for sol in solutions:
        if sol < 0:
            return
        if not np.isclose(sol - np.round(sol), 0, atol=0.001):
            return

    return int(round(solutions[0])), int(round(solutions[1]))


def solve(matrix: Matrix) -> tuple[int, int] | None:
    """
    Solves the system of equations and returns the solution. Returns
    None if the solution cannot be determined.
    """
    try:
        solution = np.linalg.solve(np.array(matrix[0]), np.array(matrix[1]))
        return verify_solutions(tuple(solution))
    except np.linalg.LinAlgError:
        return


def solve_all(matrices: list[Matrix]) -> int:
    """Solves all of the system of equations in matrices"""
    total_cost = 0
    for matrix in matrices:
        sol = solve(matrix)
        if sol:
            total_cost += (3*sol[0] + sol[1])
    return total_cost


def sol_1_wrapper(data: list[str]) -> int:
    """Wrapper function to get solution 1"""
    data_chunks = create_data_chunks(data)
    matrices = create_matrices(data_chunks)
    return solve_all(matrices)


def sol_2_wrapper(data: list[str]) -> int:
    """Wrapper function to get solution 2"""
    data_chunks = create_data_chunks(data)
    matrices = create_matrices(data_chunks, modify=True)
    return solve_all(matrices)


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    data = extract_data_to_list(13)
    sol_1 = sol_1_wrapper(data)
    sol_2 = sol_2_wrapper(data)
    return sol_1, sol_2
