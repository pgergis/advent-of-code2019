from utils.intcode import IntcodeComputer
from enum import Enum


class Color(Enum):
    BLACK = 0
    WHITE = 1


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


DELTAS = {
    Direction.UP: (0, 1),
    Direction.DOWN: (0, -1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
}


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = Color.BLACK

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))


class Hull:
    GRID_SIZE = 200
    panels = {}

    def get_color(self, pos: Position):
        if pos in self.panels:
            return self.panels[pos].color
        else:
            new_pos = Position(pos.x, pos.y)
            self.panels[new_pos] = new_pos
            return new_pos.color

    def set_color(self, pos: Position, color: Color):
        orig_color = self.get_color(pos)
        self.panels[pos].color = color
        if orig_color == self.panels[pos].color:
            return False
        return True

    def display_hull(self):
        initial_grid = [
            ["." for i in range(self.GRID_SIZE)] for j in range(self.GRID_SIZE)
        ]
        origin = (self.GRID_SIZE // 2, self.GRID_SIZE // 2)
        for p in self.panels.keys():
            x_offset, y_offset = p.x, p.y
            x_origin, y_origin = origin
            initial_grid[x_origin + y_offset][y_origin + x_offset] = (
                "#" if p.color == Color.WHITE else "."
            )
        for row in initial_grid[::-1]:
            for column in row:
                print(column, end="")
            print("")


class Robot:
    position = Position(0, 0)
    direction = Direction.UP
    visited = {position}

    def __init__(self, prog, hull=Hull(), start_on_white=False):
        self.hull = hull
        self.io_buffer = []
        self.brain = IntcodeComputer(prog, io_buffer=self.io_buffer)

        if start_on_white:
            self.hull.set_color(self.position, Color.WHITE)

    def update_io(self):
        self.io_buffer.append(self.hull.get_color(self.position).value)

    def paint_hull(self):
        self.update_io()
        while self.brain.run(halt_on_output=True) == 1:
            if len(self.io_buffer) == 2:
                direction, color = self.io_buffer.pop(), self.io_buffer.pop()
                self.paint_position(Color(color))
                self.turn(direction)
                self.move_forward()
                self.update_io()

    def paint_position(self, color):
        self.visited.add(self.position)
        self.hull.set_color(self.position, color)

    def move_forward(self):
        new_x, new_y = DELTAS[self.direction]
        self.position = Position(self.position.x + new_x, self.position.y + new_y)

    def turn(self, next_dir):
        if next_dir == 1:
            n = self.direction.value + 1
        else:
            n = self.direction.value - 1

        self.direction = Direction(n % 4)


def run_test():
    r = Robot(["99"])
    seq = [(1, 0), (0, 0), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0)]
    for color, direction in seq:
        color = Color(color)
        hull_color = r.hull.get_color(r.position)
        print(f"Painting {r.position} {color} from {hull_color}")
        r.paint_position((color))
        r.turn(direction)
        r.move_forward()

    assert len(r.visited) == 6

    r.hull.GRID_SIZE = 5
    r.hull.display_hull()


if __name__ == "__main__":
    from utils.cli import lines_in

    r1 = Robot(lines_in)
    r1.paint_hull()
    print("q1", len(r1.visited))

    r2 = Robot(lines_in, start_on_white=True)
    r2.paint_hull()
    r2.hull.display_hull()
