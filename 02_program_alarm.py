from itertools import combinations
from utils.file_parser import lines_in
from utils.intcode import IntcodeComputer

tape = IntcodeComputer(lines_in)
tape.set_inputs(12, 2)
print("q1:", tape.run()[0])

DESIRED_OUTPUT = 19690720
for noun, verb in combinations(range(0, 100), 2):
    tape.set_inputs(noun, verb)
    if tape.run()[0] == DESIRED_OUTPUT:
        print("q2:", 100 * noun + verb)
        break
