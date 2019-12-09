from utils.cli import lines_in
from utils.intcode import IntcodeComputer

tape = IntcodeComputer(lines_in)
print("NOTE: For part 1, enter input 1; for part2, enter input 2")
tape.run()
