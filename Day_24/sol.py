from typing import Callable
from utils.utils import extract_data_to_list


Wires = tuple[str, str, str]
Gate = Callable[[str, str, str, dict[str, int]], None]
Circuit = list[tuple[Wires, Gate]]
Circuit_Map = dict[str, tuple[str, str, Gate]]


def AND(w1: str, w2: str, w3: str, wire_vals: dict[str, int]) -> None:
    """Sets the output_wire to 1 if wire_1 and wire_2 are both 1"""
    wire_vals[w3] = 1 if wire_vals[w1] and wire_vals[w2] else 0
    return


def OR(w1: str, w2: str, w3: str, wire_vals: dict[str, int]) -> None:
    """Sets the output_wire to 1 if wire_1 and wire_2 are both 1"""
    wire_vals[w3] = 1 if wire_vals[w1] or wire_vals[w2] else 0
    return


def XOR(w1: str, w2: str, w3: str, wire_vals: dict[str, int]) -> None:
    """Sets the output_wire to 1 if wire_1 and wire_2 are both 1"""
    wire_vals[w3] = 1 if wire_vals[w1] != wire_vals[w2] else 0
    return


def initial_vals(data: list[str]) -> dict[str, int]:
    """Returns a dictionary with the wire's initial condition"""
    return {wire: int(val) for row in data for wire, val in [row.split(': ')]}


def init_connections(data: list[str]) -> Circuit:
    """Returns a circuit"""
    gate_map = {'AND': AND, 'OR': OR, 'XOR': XOR}
    circuit = []
    for row in data:
        inputs, output = row.split(' -> ')
        w1, gate, w2 = inputs.split(' ')
        circuit.append(((w1, w2, output), gate_map[gate]))
    return circuit


def init_circuit(data: list[str]) -> tuple[dict[str, int], Circuit]:
    """
    Returns a dictionary with the initial values of the wires and a circuit
    """
    for idx, row in enumerate(data):
        if not row:
            return initial_vals(data[:idx]), init_connections(data[idx+1:])


def start_circuit(wire_vals: dict[str, int], connections: Circuit) -> None:
    """Updates wire_vals until connections is empty"""
    processed_map = {}
    while len(processed_map.keys()) < len(connections):
        for idx, connection in enumerate(connections):
            if processed_map.get(idx):
                continue
            wires, gate = connection
            w1, w2, w3 = wires
            if wire_vals.get(w1) is not None and wire_vals.get(w2) is not None:
                gate(w1, w2, w3, wire_vals)
                processed_map[idx] = True


def get_solution_1(wire_vals: dict[str, int]) -> int:
    """Returns the decimal of the concatenation z wires"""
    z_wires = sorted(
        [wire for wire in wire_vals if wire.startswith('z')], reverse=True
    )
    return int(''.join([str(wire_vals[wire]) for wire in z_wires]), 2)


# Credit to HyperNeutrino for the logic - part 2 definitely escaped me
def make_wire(char: str, num: int) -> str:
    """Returns a wire number based on the given inputs"""
    return char + str(num).rjust(2, '0')


def create_circuit_dict(circuit: Circuit) -> Circuit_Map:
    """Returns a circuit dict to make part 2 easier"""
    circuit_dict = {}
    for connection in circuit:
        wires, gate = connection
        w1, w2, w3 = wires
        circuit_dict[w3] = (w1, w2, gate)
    return circuit_dict


def verify_z_wire(z_wire: str, num: int, circuit_map: Circuit_Map) -> bool:
    w1, w2, gate = circuit_map[z_wire]
    if gate != XOR:
        return False
    if num == 0:
        return sorted([w1, w2]) == ['x00', 'y00']
    return (
        verify_inter_xor(w1, num, circuit_map)
        and verify_carry_bit(w2, num, circuit_map)
        or verify_inter_xor(w2, num, circuit_map)
        and verify_carry_bit(w1, num, circuit_map)
    )


def verify_inter_xor(wire: str, num: int, circuit_map: Circuit_Map):
    if not circuit_map.get(wire):
        return False
    w1, w2, gate = circuit_map[wire]
    if gate != XOR:
        return False
    return sorted([w1, w2]) == [make_wire('x', num), make_wire('y', num)]


def verify_carry_bit(wire: str, num: int, circuit_map: Circuit_Map) -> bool:
    if not circuit_map.get(wire):
        return False
    w1, w2, gate = circuit_map[wire]
    if num == 1:
        if gate != AND:
            return False
        return sorted([w1, w2]) == ['x00', 'y00']

    if gate != OR:
        return False
    return (
        verify_direct_carry(w1, num-1, circuit_map)
        and verify_recarry(w2, num-1, circuit_map)
        or verify_direct_carry(w2, num-1, circuit_map)
        and verify_recarry(w1, num-1, circuit_map)
    )


def verify_direct_carry(wire: str, num: int, circuit_map: Circuit_Map) -> bool:
    if not circuit_map.get(wire):
        return False
    w1, w2, gate = circuit_map[wire]
    if gate != AND:
        return False
    return sorted([w1, w2]) == [make_wire('x', num), make_wire('y', num)]


def verify_recarry(wire: str, num: int, circuit_map: Circuit_Map) -> bool:
    if not circuit_map.get(wire):
        return False
    w1, w2, gate = circuit_map[wire]
    if gate != AND:
        return False
    return (
        verify_inter_xor(w1, num, circuit_map)
        and verify_carry_bit(w2, num, circuit_map)
        or verify_inter_xor(w2, num, circuit_map)
        and verify_carry_bit(w1, num, circuit_map)
    )


def progress(circuit_map: Circuit_Map) -> int:
    i = 0
    while True:
        if not verify_z_wire(make_wire('z', i), i, circuit_map):
            break
        i += 1
    return i


def get_solution_2(circuit_map: Circuit_Map):
    swaps = []
    for _ in range(4):
        base_line = progress(circuit_map)
        for x in circuit_map:
            for y in circuit_map:
                if x == y:
                    continue
                circuit_map[x], circuit_map[y] = circuit_map[y], circuit_map[x]
                if progress(circuit_map) > base_line:
                    break
                circuit_map[x], circuit_map[y] = circuit_map[y], circuit_map[x]
            else:
                continue
            break
        swaps.extend([x, y])
    return ','.join(sorted(swaps))


def solution() -> tuple[int, int]:
    """Returns a solution as a tuple of ints"""
    wire_vals, circuit = init_circuit(extract_data_to_list(24))
    start_circuit(wire_vals, circuit)
    return (
        get_solution_1(wire_vals), get_solution_2(create_circuit_dict(circuit))
    )
