import os

PARENT_DIR = os.path.dirname(os.path.dirname(__file__))


def build_fp(day: int) -> str:
    return os.path.join(PARENT_DIR, f"Day_{day}", "input.txt")


def extract_data_to_list(day: int) -> list[str]:
    """
    Returns a list of all of the lines found in the day's input.txt
    file (i.e., ./Day_{day}/input.txt). Removes the '\n' character
    from each line.
    """
    fp = build_fp(day)

    with open(fp, "r") as file_obj:
        data = [line.strip() for line in file_obj.readlines()]
    return data


def extract_data_to_list_of_list(day: int) -> list[list[str]]:
    """
    Returns a list of list of characters found in a day's input.txt
    file. Removes the '\n' character.
    """
    return [list(row) for row in extract_data_to_list(day)]


def merge_strings(data: list[str]) -> str:
    """Returns one string composed of all of the strings in the input"""
    merged_string = ""
    for item in data:
        merged_string += item
    return merged_string


def get_raw_input_stream(day: int) -> str:
    """Returns the raw string data from the input in one string"""
    fp = build_fp(day)

    with open(fp, "r") as file_obj:
        data = [line for line in file_obj.readlines()]
    return merge_strings(data)
