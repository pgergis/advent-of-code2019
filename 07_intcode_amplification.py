import itertools
from utils.intcode import IntcodeComputer


def run_amp_loop(phase_range, feedback_mode):
    outputs = []
    for io_order in map(list, itertools.permutations(phase_range, 5)):
        io = [0]
        a, b, c, d, e = (
            IntcodeComputer(lines_in, io_buffer=io),
            IntcodeComputer(lines_in, io_buffer=io),
            IntcodeComputer(lines_in, io_buffer=io),
            IntcodeComputer(lines_in, io_buffer=io),
            IntcodeComputer(lines_in, io_buffer=io),
        )

        not_halted = [a, b, c, d, e]
        for comp in not_halted:
            if io_order:
                io.append(io_order.pop())
            if comp.run(halt_on_output=feedback_mode) == 1:
                not_halted.append(comp)

        outputs.append(io.pop())
    return max(outputs)


if __name__ == "__main__":
    from utils.cli import lines_in

    print("pt. 1", run_amp_loop(range(5), False))
    print("pt. 2", run_amp_loop(range(5, 10), True))
