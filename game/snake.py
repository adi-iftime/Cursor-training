# DAG owner: data_engineer (game runtime domain) — movement primitives.
"""Snake entity and direction helpers (pure logic)."""

from __future__ import annotations

from enum import IntEnum
from typing import List, Tuple

Point = Tuple[int, int]


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


_VEC: dict[Direction, Point] = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}


def opposite(a: Direction, b: Direction) -> bool:
    return (a + 2) % 4 == b


def next_cell(head: Point, direction: Direction) -> Point:
    dr, dc = _VEC[direction]
    return (head[0] + dr, head[1] + dc)


class Snake:
    __slots__ = ("body", "direction")

    def __init__(self, body: List[Point], direction: Direction) -> None:
        if len(body) < 1:
            raise ValueError("snake needs at least one segment")
        self.body = body
        self.direction = direction

    def head(self) -> Point:
        return self.body[0]

    def advance(self, new_direction: Direction, *, eat: bool) -> None:
        if not opposite(new_direction, self.direction):
            self.direction = new_direction
        dr, dc = _VEC[self.direction]
        hr, hc = self.head()
        new_head = (hr + dr, hc + dc)
        self.body.insert(0, new_head)
        if eat:
            return
        self.body.pop()
