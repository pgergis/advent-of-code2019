from collections import namedtuple
from enum import Enum
import typing

Point = namedtuple("Point", "x y")
ORIGIN = Point(0, 0)


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


def nextPoint(start: Point, direction: Direction) -> Point:
    if direction == Direction.UP:
        return Point(start.x, start.y + 1)
    if direction == Direction.DOWN:
        return Point(start.x, start.y - 1)
    if direction == Direction.LEFT:
        return Point(start.x - 1, start.y)
    if direction == Direction.RIGHT:
        return Point(start.x + 1, start.y)

    return Point(start.x, start.y)


def gridDistance(start: Point, end: Point) -> int:
    return sum(map(abs, [start.x - end.x, start.y - end.y]))


def buildPath(movements: [str]) -> typing.List[Point]:
    path = [ORIGIN]
    for direction, count in map(lambda s: (s[0], s[1:]), movements):
        for _ in range(int(count)):
            path.append(nextPoint(path[-1], Direction(direction)))

    return path


def intersections(path1: [Point], path2: [Point]) -> typing.Set[Point]:
    return set(path1) & set(path2) - {ORIGIN}


def stepsToPoint(point: Point, path: [Point]) -> int:
    return path.index(point)


if __name__ == "__main__":
    from utils.cli import lines_in

    assert len(lines_in) == 2

    path1 = buildPath(lines_in[0].split(","))
    path2 = buildPath(lines_in[1].split(","))
    intersections = [
        (
            point,
            gridDistance(ORIGIN, point),
            stepsToPoint(point, path1) + stepsToPoint(point, path2),
        )
        for point in intersections(path1, path2)
    ]

    print("q1", sorted(intersections, key=lambda pds: pds[1])[0][1])
    print("q2", sorted(intersections, key=lambda pds: pds[2])[0][2])
