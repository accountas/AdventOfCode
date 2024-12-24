from common.data import *
from dataclasses import dataclass
from time import time
from itertools import combinations


@dataclass(frozen=True)
class Gate:
    a: str
    b: str
    output: str
    operation: str

    def __repr__(self):
        return f"{self.a} {self.operation} {self.b} -> {self.output}"

    def with_output(self, output):
        return Gate(self.a, self.b, output, self.operation)

    def compute(self, a, b):
        if self.operation == "AND":
            return a & b
        elif self.operation == "OR":
            return a | b
        elif self.operation == "XOR":
            return a ^ b
        else:
            raise ValueError(f"Unknown operation: {self.operation}")


def parse_input(input):
    raw_states, raw_gates = input.split("\n\n")

    states = {}
    for state in raw_states.splitlines():
        wire, value = state.split(": ")
        value = int(value)
        states[wire] = value

    gates = {}
    for gate in raw_gates.splitlines():
        a, operation, b, _, output = gate.split()
        gate = Gate(a, b, output, operation)
        gates[output] = gate

    return states, gates


def is_input(wire):
    return wire[0] in "xy"


def subtrees_match(node_left, node_right, gates_left, gates_right):
    if is_input(node_left) and is_input(node_right):
        return node_left == node_right

    if is_input(node_left) != is_input(node_right):
        return False

    gate_left = gates_left[node_left]
    gate_right = gates_right[node_right]

    if gate_left.operation != gate_right.operation:
        return False

    if subtrees_match(
        gate_left.a, gate_right.a, gates_left, gates_right
    ) and subtrees_match(gate_left.b, gate_right.b, gates_left, gates_right):
        return True

    if subtrees_match(
        gate_left.a, gate_right.b, gates_left, gates_right
    ) and subtrees_match(gate_left.b, gate_right.a, gates_left, gates_right):
        return True

    return False


def fix_circuit(cur_bit, gates, target, swaps):
    cur_wire = f"z{cur_bit:02}"

    if cur_bit == 46:
        return swaps

    if subtrees_match(cur_wire, cur_wire, gates, target):
        return fix_circuit(cur_bit + 1, gates, target, swaps)

    for gate_a, gate_b in combinations(gates.values(), 2):
        gates[gate_a.output] = gate_b.with_output(gate_a.output)
        gates[gate_b.output] = gate_a.with_output(gate_b.output)

        if subtrees_match(cur_wire, cur_wire, gates, target):
            return fix_circuit(
                cur_bit + 1, gates, target, swaps + [gate_a.output, gate_b.output]
            )

        gates[gate_a.output] = gate_a
        gates[gate_b.output] = gate_b


def to_graphviz(gates):
    lines = set()
    for gate in gates.values():
        lines.add(f'{gate.output} -> {gate.a} [label = "{gate.operation}", ];')
        lines.add(f'{gate.output} -> {gate.b} [label = "{gate.operation}"];')
    print("\n".join(lines))


def build_good_adder(num_bits):
    """
    https://upload.wikimedia.org/wikipedia/commons/5/57/Fulladder.gif
    """

    wires = {}

    wires["z00"] = Gate("x00", "y00", "z00", "XOR")
    wires["car_00"] = Gate("x00", "y00", "car_00", "AND")

    last_carry = "car_00"
    for bit_id in range(1, num_bits):
        input_x = f"x{bit_id:02}"
        input_y = f"y{bit_id:02}"
        sum_xy = f"sum_xy_{bit_id:02}"
        output_bit = f"z{bit_id:02}"

        carry_xy = f"carry_xy_{bit_id:02}"
        carry_xyc = f"carry_xyc_{bit_id:02}"

        if bit_id < num_bits - 1:
            next_carry = f"car_{bit_id:02}"
        else:
            next_carry = f"z{num_bits:02}"

        wires[sum_xy] = Gate(input_x, input_y, sum_xy, "XOR")
        wires[output_bit] = Gate(sum_xy, last_carry, output_bit, "XOR")
        wires[carry_xy] = Gate(input_x, input_y, carry_xy, "AND")
        wires[carry_xyc] = Gate(sum_xy, last_carry, carry_xyc, "AND")
        wires[next_carry] = Gate(carry_xy, carry_xyc, next_carry, "OR")
        last_carry = next_carry

    return wires


def compute(wire, states, gates):
    if wire in states:
        return states[wire]

    gate = gates[wire]
    a = compute(gate.a, states, gates)
    b = compute(gate.b, states, gates)
    states[gate.output] = gate.compute(a, b)

    return states[wire]


def test_circuit(x, y, gates):
    bin_x = bin(x)[2:].zfill(45)
    bin_y = bin(y)[2:].zfill(45)

    states = {}

    for i in range(45):
        states[f"x{i:02}"] = int(bin_x[::-1][i])
        states[f"y{i:02}"] = int(bin_y[::-1][i])

    for gate in gates.values():
        compute(gate.output, states, gates)

    z_values = [states[f"z{i:02}"] for i in range(46)]

    return int("".join(str(state) for state in z_values)[::-1], 2)


def main():
    input = get_data(year=2024, day=24, sample=False)
    states, bad_adder = parse_input(input)

    input_x = int("".join(str(states[f"x{i:02}"]) for i in range(45))[::-1], 2)
    input_y = int("".join(str(states[f"y{i:02}"]) for i in range(45))[::-1], 2)
    print("part 1:", test_circuit(input_x, input_y, bad_adder))

    good_adder = build_good_adder(45)
    swaps = sorted(fix_circuit(1, bad_adder, good_adder, []))

    assert test_circuit(input_x, input_y, bad_adder) == input_x + input_y

    print("Part 2:", ",".join(swaps))


if __name__ == "__main__":
    start = time()
    main()
    print(f"Time: {time()-start:.4f} sec")
