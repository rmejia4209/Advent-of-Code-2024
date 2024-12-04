from utils.utils import extract_data_to_list


def add_padding(data: list[str]) -> list[str]:
    """Adds padding to the data"""
    top = [('-' * (len(data)+6-1)) for _ in range(3)]
    new_list = top[:]
    for string in data:
        side = '-' * 3
        new_list.append(side + string + side)
    new_list.extend(top[:])
    return new_list


def find_mas(data: list[str], row: int, col: int) -> int:
    """
    Return the number of times the characters 'mas' are found
    from row, col in data
    """
    total = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            mas_found = True
            for letter, delta in zip("MAS", [1, 2, 3]):
                if data[row+(delta*i)][col+(delta*j)] != letter:
                    mas_found = False
                    break
            total += 1 if mas_found else 0
    return total


def find_cross_mas(data: list[str], row: int, col: int) -> int:
    """Return true if a crossed mas is found from the given row and col"""
    corners = (
        data[row-1][col-1] +
        data[row-1][col+1] +
        data[row+1][col-1] +
        data[row+1][col+1]
    )
    valid_seqs = ["MSMS", "SMSM", "SSMM", "MMSS"]
    return corners in valid_seqs


def find_all_xmas(data: list[str]) -> tuple[int, int]:
    """Return the number of times the word xmas is found in given data"""
    total_xmas = 0
    total_cross_mas = 0
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == 'X':
                total_xmas += find_mas(data, row, col)
            if data[row][col] == 'A':
                total_cross_mas += 1 if find_cross_mas(data, row, col) else 0
    return total_xmas, total_cross_mas


def solution() -> tuple[int, int]:

    data = add_padding(extract_data_to_list(4))
    sol_1, sol_2 = find_all_xmas(data)

    return sol_1, sol_2
