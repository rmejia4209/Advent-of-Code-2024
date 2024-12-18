from typing import Callable
from utils.utils import extract_data_to_list

Registers = dict[str, int]
Operation = Callable[[Registers, int, int], int]
Operations = dict[int, Operation]
Stack = list[int]


def init_registers(data: list[str]) -> Registers:
    """Initializes the registers based on the data"""
    registers = {'Output': []}
    for line, register in zip(data, ['A', 'B', 'C']):
        registers[register] = int(line.split(': ')[1])
    return registers


def get_program_stack(data: list[str]) -> list[int]:
    """Gets the program stack from the data"""
    return [int(num) for num in data[-1].split(': ')[1].split(',')]


def get_operation_dict() -> Operations:
    """Returns a dict with the operations mapped to ints"""
    return {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}


def get_combo_operand(idx: int, registers: Registers) -> int:
    """Returns the combo operand of the given index"""
    if idx in [0, 1, 2, 3]:
        val = idx
    else:
        idx_to_register_key = {4: 'A', 5: 'B', 6: 'C'}
        val = registers[idx_to_register_key[idx]]
    return val


def adv(registers: Registers, operand: int, pos: int) -> int:
    """
    Divides the value in register A by 2^combo_operand and
    stores the result in A. Returns the next instruction position.
    """
    combo_operand = get_combo_operand(operand, registers)
    registers['A'] = int(registers['A'] / (2**combo_operand))
    return pos + 2


def bxl(registers: Registers, operand: int, pos: int) -> int:
    """
    Performs a bitwise xor on register b and the literal operand.
    Stores the result in register B. Returns the next instruction position.
    """
    registers['B'] = registers['B'] ^ operand
    return pos + 2


def bst(registers: Registers, operand: int, pos: int) -> int:
    """
    Stores the result of the combo operand modulo 8 and stores the result
    in register B. Returns the next instruction position.
    """
    combo_operand = get_combo_operand(operand, registers)
    registers['B'] = combo_operand % 8
    return pos + 2


def jnz(registers: Registers, operand: int, pos: int) -> int:
    """
    Jumps to the instruction at the operand if the value at register A is
    not 0. Otherwise does nothing.
    """
    return operand if registers['A'] != 0 else pos + 2


def bxc(registers: Registers, operand: int, pos: int) -> int:
    """
    Stores the bitwise xor of register B and register C in register B.
    Returns the next instruction position.
    """
    registers['B'] = registers['B'] ^ registers['C']
    return pos + 2


def out(registers: Registers, operand: int, pos: int) -> int:
    """
    Prints the value of the combo operand modulo 8. Returns the next 
    instruction position.
    """
    combo_operand = get_combo_operand(operand, registers)
    registers['Output'].append(combo_operand % 8)
    return pos + 2


def bdv(registers: Registers, operand: int, pos: int) -> int:
    """
    Divides the value in register A by 2^combo_operand and
    stores the result in B. Returns the next instruction position.
    """
    combo_operand = get_combo_operand(operand, registers)
    registers['B'] = int(registers['A'] / (2**combo_operand))
    return pos + 2


def cdv(registers: Registers, operand: int, pos: int) -> int:
    """
    Divides the value in register A by 2^combo_operand and
    stores the result in C. Returns the next instruction position.
    """
    combo_operand = get_combo_operand(operand, registers)
    registers['C'] = int(registers['A'] / (2**combo_operand))
    return pos + 2


def run_program(registers: Registers, stack: Stack) -> None:
    """Runs the instructions in the stack"""
    pos = 0
    operations = get_operation_dict()
    while pos < len(stack):
        opcode = stack[pos]
        operand = stack[pos+1]
        pos = operations[opcode](registers, operand, pos)
    return


# Credit to scorixear for the algorithm
# (although my cache needed to be set -1 not 0...)
def find_A(data: list[str], stack: Stack) -> None:
    """Returns the lowest value for A that outputs the program stack"""
    digits = [0] * len(stack)
    cache = [-1] * len(stack)
    j = len(stack)-1
    while j >= 0:
        found = False
        A = sum([digits[i]*(8**(i)) for i in range(len(stack))])
        print(f'Finding {stack[j]}')
        for i in range(cache[j]+1, 8):
            registers = init_registers(data)
            registers['A'] = A + i*(8**j)
            run_program(registers, stack)
            if len(registers['Output']) != len(stack):
                continue
            # Digit at position j matches in both the output & stack
            if registers['Output'][j] == stack[j]:
                digits[j] = i
                cache[j] = i
                found = True
                break
        if not found:
            digits[j] = 0
            digits[j+1] = 0
            cache[j] = -1
            j += 1
        else:
            j -= 1

    return sum([digits[i]*(8**(i)) for i in range(len(stack))])


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    data = extract_data_to_list(17)
    registers = init_registers(data)
    program_instructions = get_program_stack(data)
    run_program(registers, program_instructions)
    sol_1 = ",".join(map(str, registers['Output']))
    sol_2 = find_A(data, program_instructions)
    return sol_1, sol_2
