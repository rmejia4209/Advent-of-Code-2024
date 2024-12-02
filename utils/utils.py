import os

PARENT_DIR = os.path.dirname(os.path.dirname(__file__))


def extract_data(day: int) -> list[str]:
    """
    Returns a list of all of the lines found in the day's input.txt
    file (i.e., ./Day_{day}/input.txt).
    """
    fp = os.path.join(PARENT_DIR, f"Day_{day}", "input.txt")

    with open(fp, "r") as file_obj:
        data = [line.strip() for line in file_obj.readlines()]
    return data
