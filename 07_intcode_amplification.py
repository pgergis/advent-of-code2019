import itertools
from utils.cli import lines_in
from utils.intcode import IntcodeComputer

a, b, c, d, e = (
    IntcodeComputer(lines_in),
    IntcodeComputer(lines_in),
    IntcodeComputer(lines_in),
    IntcodeComputer(lines_in),
    IntcodeComputer(lines_in),
)

outputs = []
for io in map(list, itertools.permutations(range(5), 5)):
    io.insert(-1, 0)

    a.io_buffer, b.io_buffer, c.io_buffer, d.io_buffer, e.io_buffer = io, io, io, io, io
    a.run(); b.run(); c.run(); d.run(); e.run()
    outputs.append(io.pop())

print(max(outputs))
