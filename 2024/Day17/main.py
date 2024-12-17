from common.data import *


class Interpreter:
    def __init__(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.IP = 0
        self.program = program
        self.stdout = []

    def run(self):
        while self.cycle():
            pass
        return self.stdout

    def cycle(self):
        if self.IP >= len(self.program):
            return False

        opcode = self.program[self.IP]
        operand = self.program[self.IP + 1]

        match opcode:
            case 0:
                self.adv(operand)
            case 1:
                self.bxl(operand)
            case 2:
                self.bst(operand)
            case 3:
                self.jnz(operand)
            case 4:
                self.bxc()
            case 5:
                self.out(operand)
            case 6:
                self.bdv(operand)
            case 7:
                self.cdv(operand)
            case _:
                raise Exception(
                    f"Invalid opcode: {opcode}",
                )

        if opcode != 3:
            self.IP += 2

        return True

    def combo_value(self, operand):
        match operand:
            case lit if lit <= 3:
                return lit
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case _:
                raise Exception("Invalid operand", operand)

    def adv(self, operand):
        combo_value = self.combo_value(operand)
        self.A = self.A // (2**combo_value)

    def bxl(self, operand):
        self.B = self.B ^ operand

    def bst(self, operand):
        combo_value = self.combo_value(operand)
        self.B = combo_value % 8

    def jnz(self, operand):
        if self.A != 0:
            self.IP = operand
        else:
            self.IP += 2

    def bxc(self):
        self.B = self.B ^ self.C

    def out(self, operand):
        combo_value = self.combo_value(operand)
        self.stdout.append(combo_value % 8)

    def bdv(self, operand):
        combo_value = self.combo_value(operand)
        self.B = self.A // (2**combo_value)

    def cdv(self, operand):
        combo_value = self.combo_value(operand)
        self.C = self.A // (2**combo_value)


def parse_input(input):
    lines = input.splitlines()

    A = int(lines[0].split(": ")[1])
    B = int(lines[1].split(": ")[1])
    C = int(lines[2].split(": ")[1])

    program = [int(x) for x in lines[4].split(": ")[1].split(",")]

    return A, B, C, program


def brute(target, program):
    """
    Not generic, utilizes logic of the input program.
    Algorithim in the input is something like this:

    B = some transformation on A
    OUT B
    A /= 8
    JNZ 0 (if A is not zero jump to start)

    No state is persisted between iterations, so we know that:
     when A = x and the program outputs [a_1, a_2, a_3, ...]
     then if A = x // 8 the program will output [a_2, a_3, ...]

    We can use this proprty to brute force the solution:
    target = head + tail
    find all x that produce tail (recursive call)
    find all y so z * 8 + y produces head + tail
    """
    if len(target) == 0:
        yield 0
        return

    for next in brute(target[1:], program):
        for now in range(8):
            maybe = now + next * 8
            if Interpreter(maybe, 0, 0, program).run() == target:
                yield maybe


def main():
    input = get_data(year=2024, day=17, sample=False)

    A, B, C, program = parse_input(input)

    part_1 = ",".join([str(x) for x in Interpreter(A, B, C, program).run()])
    print("Part 1:", part_1)

    part_2 = next(brute(program, program))
    assert Interpreter(part_2, 0, 0, program).run() == program
    print("Part 2:", part_2)


if __name__ == "__main__":
    main()
