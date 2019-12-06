from utils.file_parser import lines_in
from utils.intcode import IntcodeComputer

tape = IntcodeComputer(lines_in)
print("NOTE: For part 1, enter input 1; for part 2, enter input 5")
tape.run()
