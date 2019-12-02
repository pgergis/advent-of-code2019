class ProgramTape:
    def __init__(self, input_lines):
        self.input_str = input_lines[0]
        self.registers = ProgramTape.initialize_tape(self.input_str)
        self.ptr = 0
        self.opcodes = {1: (self.opcode_add, 3), 2: (self.opcode_mult, 3)}

    def getVal(self, address):
        return self.registers[address]

    def setVal(self, address, val):
        self.registers[address] = val

    def callOp(self, op):
        fn, param_count = self.opcodes.get(op, (lambda args: None, 0))
        params = []
        for i in range(0, param_count):
            self.ptr += 1
            params.append(self.getVal(self.ptr))

        fn(*params)

    def reset(self):
        self.registers = ProgramTape.initialize_tape(self.input_str)
        self.ptr = 0

    def process_tape(self):
        while (op := self.getVal(self.ptr)) in self.opcodes:
            self.callOp(op)
            self.ptr += 1

        return self.registers

    def set_inputs(self, noun, verb):
        self.setVal(1, noun)
        self.setVal(2, verb)

    def opcode_add(self, locX, locY, dest):
        x = self.getVal(locX)
        y = self.getVal(locY)
        self.setVal(dest, x + y)

    def opcode_mult(self, locX, locY, dest):
        x = self.getVal(locX)
        y = self.getVal(locY)
        self.setVal(dest, x * y)

    @staticmethod
    def initialize_tape(input_str):
        return list(map(int, input_str.split(",")))


if __name__ == "__main__":
    from itertools import combinations
    from utils.file_parser import lines_in

    tape = ProgramTape(lines_in)
    tape.set_inputs(12, 2)
    print("q1:", tape.process_tape()[0])
    tape.reset()

    DESIRED_OUTPUT = 19690720
    for noun, verb in combinations(range(0, 100), 2):
        tape.set_inputs(noun, verb)
        if tape.process_tape()[0] == DESIRED_OUTPUT:
            print("q2:", 100 * noun + verb)
            break
        tape.reset()
