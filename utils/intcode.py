from enum import Enum


OPCODE_LENGTH = 2


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class IntcodeComputer:
    def __init__(self, input_lines):
        self.input_str = input_lines[0]

        self.registers = IntcodeComputer.initialize_tape(self.input_str)
        self.ptr = 0

    def getVal(self, address):
        return self.registers[address]

    def setVal(self, address, val):
        self.registers[address] = val

    def performInstruction(self, fn, param_modes):
        params = []
        for p_mode in param_modes[::-1]:
            self.ptr += 1
            val_at_pointer = self.getVal(self.ptr)
            if p_mode == ParameterMode.POSITION:
                params.append(self.getVal(val_at_pointer))
            elif p_mode == ParameterMode.IMMEDIATE:
                params.append(val_at_pointer)
            else:
                raise TypeError("Undefined ParameterMode!?")

        return fn(*params, self)

    def reset(self):
        self.registers = IntcodeComputer.initialize_tape(self.input_str)
        self.ptr = 0

    def run(self, reset=True):
        while (instruction := Instruction(str(self.getVal(self.ptr)))) :
            if instruction.opcode == Instruction.TERMINATE_CODE:
                break
            self.ptr = self.performInstruction(instruction.fn, instruction.param_modes)
            if self.ptr >= len(self.registers):
                raise TypeError("Out of registers!!")

        final_state = self.registers
        if reset:
            self.reset()
        return final_state

    def set_inputs(self, noun, verb):
        self.setVal(1, noun)
        self.setVal(2, verb)

    @staticmethod
    def opcode_add(x, y, dest, tape):
        tape.setVal(dest, x + y)
        return tape.ptr + 1

    @staticmethod
    def opcode_mult(x, y, dest, tape):
        tape.setVal(dest, x * y)
        return tape.ptr + 1

    @staticmethod
    def opcode_output(pos, tape):
        print(tape.getVal(pos))
        return tape.ptr + 1

    @staticmethod
    def opcode_input(dest, tape):
        val_in = int(input("taking input: "))
        tape.setVal(dest, val_in)
        return tape.ptr + 1

    @staticmethod
    def opcode_jump_if_true(p, jump_to, tape):
        if p:
            return jump_to
        return tape.ptr + 1

    @staticmethod
    def opcode_jump_if_false(p, jump_to, tape):
        if not p:
            return jump_to
        return tape.ptr + 1

    @staticmethod
    def opcode_less_than(a, b, dest, tape):
        if a < b:
            tape.setVal(dest, 1)
        else:
            tape.setVal(dest, 0)

        return tape.ptr + 1

    @staticmethod
    def opcode_eq(a, b, dest, tape):
        if a == b:
            tape.setVal(dest, 1)
        else:
            tape.setVal(dest, 0)

        return tape.ptr + 1

    @staticmethod
    def initialize_tape(input_str):
        return list(map(int, input_str.split(",")))


class Instruction:
    TERMINATE_CODE = 99
    OPCODE_FN_MAP = {
        1: (IntcodeComputer.opcode_add, "100"),
        2: (IntcodeComputer.opcode_mult, "100"),
        3: (IntcodeComputer.opcode_input, "1",),
        4: (IntcodeComputer.opcode_output, "1"),
        5: (IntcodeComputer.opcode_jump_if_true, "00"),
        6: (IntcodeComputer.opcode_jump_if_false, "00"),
        7: (IntcodeComputer.opcode_less_than, "100"),
        8: (IntcodeComputer.opcode_eq, "100"),
        TERMINATE_CODE: (lambda args: None, "0"),
    }

    def __init__(self, instruction):
        op_in, params_in = instruction[-OPCODE_LENGTH:], instruction[:-OPCODE_LENGTH].zfill(1)
        self.opcode = int(op_in)

        self.fn, default_param_modes = self.getFnForOpcode()
        set_params = "{:b}".format(int(params_in, base=2) | int(default_param_modes, base=2)).zfill(
            len(default_param_modes)
        )
        self.param_modes = [ParameterMode(int(p)) for p in set_params]

    def getFnForOpcode(self):
        # returns mapped function and default parameter modes in a tuple
        try:
            op_fn, default_params = self.OPCODE_FN_MAP[self.opcode]
            return op_fn, default_params
        except Exception:
            raise ValueError(f"Invalid Opcode!", self.opcode)
