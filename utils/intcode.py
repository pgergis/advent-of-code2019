from enum import Enum


OPCODE_LENGTH = 2


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2
    RELATIVE_POS = 3


class IntcodeComputer:
    def __init__(self, input_lines):
        self.input_str = input_lines[0]

        self.registers = IntcodeComputer.initialize_tape(self.input_str) + [0] * 10000
        self.ptr = 0
        self.relative_base = 0

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
                param_val = self.getVal(val_at_pointer)
            elif p_mode == ParameterMode.IMMEDIATE:
                param_val = val_at_pointer
            elif p_mode == ParameterMode.RELATIVE:
                param_val = self.getVal(self.relative_base + val_at_pointer)
            elif p_mode == ParameterMode.RELATIVE_POS:
                param_val = self.relative_base + val_at_pointer
            else:
                raise TypeError("Undefined ParameterMode!?")
            params.append(param_val)
            # print(p_mode, val_at_pointer, param_val)

        return fn(*params, self)

    def reset(self):
        self.registers = IntcodeComputer.initialize_tape(self.input_str)
        self.ptr = 0

    def run(self, reset=True):
        while (instruction := Instruction(str(self.getVal(self.ptr)))) :
            # print(self.relative_base, self.ptr)
            # print(self.registers[max(self.ptr-10,0):self.ptr+10])
            if instruction.opcode == Instruction.TERMINATE_CODE:
                break
            self.ptr = self.performInstruction(instruction.fn, instruction.param_modes)
            if self.ptr >= len(self.registers):
                raise TypeError("Out of registers!!")

        final_state = self.registers
        if reset:
            self.reset()

    def set_inputs(self, noun, verb):
        self.setVal(1, noun)
        self.setVal(2, verb)

    @staticmethod
    def opcode_add(x, y, dest, tape):
        # print("adding", x, y, dest)
        tape.setVal(dest, x + y)
        return tape.ptr + 1

    @staticmethod
    def opcode_mult(x, y, dest, tape):
        # print("multiplying", x, y, dest)
        tape.setVal(dest, x * y)
        return tape.ptr + 1

    @staticmethod
    def opcode_output(val, tape):
        # print("outputting", val)
        print(val)
        return tape.ptr + 1

    @staticmethod
    def opcode_input(dest, tape):
        val_in = int(input("taking input: "))
        tape.setVal(dest, val_in)
        return tape.ptr + 1

    @staticmethod
    def opcode_jump_if_true(p, jump_to, tape):
        # print(f"jumping to {jump_to} if {p}")
        if p:
            return jump_to
        return tape.ptr + 1

    @staticmethod
    def opcode_jump_if_false(p, jump_to, tape):
        # print(f"jumping to {jump_to} if NOT {p}")
        if not p:
            return jump_to
        return tape.ptr + 1

    @staticmethod
    def opcode_less_than(a, b, dest, tape):
        # print(f"setting {dest} to {a} < {b}")
        tape.setVal(dest, int(a < b))
        return tape.ptr + 1

    @staticmethod
    def opcode_eq(a, b, dest, tape):
        # print(f"setting {dest} to {a} == {b}")
        tape.setVal(dest, int(a == b))
        return tape.ptr + 1

    @staticmethod
    def opcode_adjust_relative_base(base_mod, tape):
        # print("adjusting relative base by", base_mod)
        tape.relative_base += base_mod
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
        4: (IntcodeComputer.opcode_output, "0"),
        5: (IntcodeComputer.opcode_jump_if_true, "00"),
        6: (IntcodeComputer.opcode_jump_if_false, "00"),
        7: (IntcodeComputer.opcode_less_than, "100"),
        8: (IntcodeComputer.opcode_eq, "100"),
        9: (IntcodeComputer.opcode_adjust_relative_base, "0"),
        TERMINATE_CODE: (lambda args: None, "0"),
    }

    def __init__(self, instruction):
        # print(instruction)
        op_in, params_in = (
            instruction[-OPCODE_LENGTH:],
            instruction[:-OPCODE_LENGTH].zfill(1),
        )
        self.opcode = int(op_in)

        self.fn, default_param_modes = self.getFnForOpcode()
        set_params = [
            int(p_in) + int(def_in)
            for p_in, def_in in zip(
                params_in.zfill(len(default_param_modes)), default_param_modes
            )
        ]
        # set_params = "{:b}".format(
        #     int(params_in, base=2) | int(default_param_modes, base=2)
        # ).zfill(len(default_param_modes))
        self.param_modes = [ParameterMode(p) for p in set_params]

    def getFnForOpcode(self):
        # returns mapped function and default parameter modes in a tuple
        try:
            op_fn, default_params = self.OPCODE_FN_MAP[self.opcode]
            return op_fn, default_params
        except Exception:
            raise ValueError(f"Invalid Opcode!", self.opcode)
