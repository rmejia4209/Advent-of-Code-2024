from utils.utils import get_raw_input_stream


Numbers = list[int]
Disk = list[int, str]


def convert_to_numbers(data: str) -> Numbers:
    """Returns a list of numbers based on string input"""
    return [int(char) for char in data]


def convert_to_disk_format(blocks: Numbers) -> Disk:
    """Returns a list representing the memory block input"""

    mem_id = 0
    mem: Disk = []
    in_use = True
    for block in blocks:
        mem.extend([mem_id if in_use else '.'] * block)
        mem_id += 1 if in_use else 0
        in_use = not in_use
    return mem


def next_empty_block(disk: Disk, start: int) -> int:
    """Returns the position of the next element that is empty"""
    for idx in range(start, len(disk)):
        if disk[idx] == '.':
            return idx


def next_empty_block_2(disk: Disk, size: int, end: int) -> int:
    """
    Returns the position of th next block with the given
    size that does not exceed end
    """
    block_size = 0
    idx = 0
    while idx < end:
        block_size = block_size + 1 if disk[idx] == '.' else 0
        if block_size == size:
            return idx - block_size + 1
        idx += 1
    return -1


def get_mem_chunk_start(disk: Disk, end: int) -> int:
    """Returns a the start of a memory chunk given the end"""
    mem_id = disk[end]
    start = 0
    for idx in range(end, -1, -1):
        if disk[idx] != mem_id:
            start = idx + 1
            break
    return start


def swap_blocks(disk: Disk, new_start: int, old_start: int, size: int) -> None:
    """Swaps data block from the old start to the new start"""
    for _ in range(size):
        disk[new_start], disk[old_start] = disk[old_start], disk[new_start]
        new_start += 1
        old_start += 1
    return


def compress_disk(disk: Disk) -> None:
    """Moves blocks from end of list to empty positions near the front"""
    start = next_empty_block(disk, 0)
    end = len(disk)-1
    while start < end:
        if disk[end] != '.':
            disk[start], disk[end] = disk[end], disk[start]
            start = next_empty_block(disk, start)
        end -= 1


def compress_disk_2(disk: Disk) -> None:
    """Moves blocks from end that can fit fully into a more left area"""
    end = len(disk) - 1
    while end > 0:
        if disk[end] != '.':
            old_start = get_mem_chunk_start(disk, end)
            size = end - old_start + 1
            new_start = next_empty_block_2(disk, size, end)
            if new_start != -1:
                swap_blocks(disk, new_start, old_start, size)
            end = old_start
        end -= 1
    return


def calculate_check_sum(disk: Disk) -> int:
    """Returns the checksum of the given disk"""
    return sum([idx * val for idx, val in enumerate(disk) if val != '.'])


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    data = convert_to_numbers(get_raw_input_stream(9))
    disk = convert_to_disk_format(data)
    compress_disk(disk)
    sol_1 = calculate_check_sum(disk)

    disk = convert_to_disk_format(data)
    compress_disk_2(disk)
    sol_2 = calculate_check_sum(disk)

    return sol_1, sol_2
