from utils.utils import extract_data_to_list


Pin_Height = tuple[int, ...]
Keys = list[Pin_Height]
Locks = list[Pin_Height]


def get_pin_height(schematic: list[list[str]]) -> Pin_Height:
    """Returns the pin height of the given schematic"""
    pin_heights = [-1] * len(schematic[0])
    for vals in schematic:
        for col, val in enumerate(vals):
            pin_heights[col] += 1 if val == '#' else 0
    return tuple(pin_heights)


def create_key_or_lock(
    locks: Locks, keys: Keys, schematic: list[list[str]]
) -> None:
    """
    Appends the pin height of the schematic to either the keys or locks
    depending on the schematic's first value
    """
    if schematic[0][0] == '#':
        locks.append(get_pin_height(schematic))
    else:
        keys.append(get_pin_height(schematic))
    schematic.clear()


def create_keys_and_locks(data: list[str]) -> tuple[Keys, Locks]:
    """Returns the keys and locks from the input data"""

    schematic, locks, keys = [], [], []
    for row in data:
        if not row:
            create_key_or_lock(locks, keys, schematic)
            continue
        schematic.append(list(row))
    create_key_or_lock(locks, keys, schematic)
    return keys, locks


def is_match(key: Pin_Height, lock: Pin_Height) -> bool:
    """Returns true if key and lock do not exceed 5"""

    for idx in range(len(key)):
        if key[idx] + lock[idx] > 5:
            return False
    return True


def matches(locks: Locks, keys: Keys) -> int:
    """Returns the number of matches between all the locks and keys"""
    total = 0
    for key in keys:
        for lock in locks:
            total += 1 if is_match(key, lock) else 0
    return total


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    keys, locks = create_keys_and_locks(extract_data_to_list(25))

    return matches(locks, keys), None
