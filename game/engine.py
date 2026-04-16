"""Game rules and stepping (Game Engine Agent). Pure logic — no terminal I/O."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Tuple

from config.settings import GRID_HEIGHT, GRID_WIDTH, POINTS_PER_FOOD
from game.snake import Direction, Snake, next_cell, opposite

PointT = Tuple[int, int]


def _empty_cell(rng: random.Random, width: int, height: int, occupied: set[PointT]) -> PointT:
    for _ in range(width * height * 2):
        r = rng.randrange(height)
        c = rng.randrange(width)
        p = (r, c)
        if p not in occupied:
            return p
    raise RuntimeError("no empty cell for food")


@dataclass
class GameEngine:
    width: int = GRID_WIDTH
    height: int = GRID_HEIGHT
    rng: random.Random = field(default_factory=random.Random)
    snake: Snake = field(init=False)
    food: PointT = field(init=False)
    score: int = 0
    game_over: bool = False
    pending_direction: Direction = Direction.RIGHT

    def __post_init__(self) -> None:
        mid_r, mid_c = self.height // 2, self.width // 2
        start_body: list[PointT] = [(mid_r, mid_c), (mid_r, mid_c - 1), (mid_r, mid_c - 2)]
        self.snake = Snake(list(start_body), Direction.RIGHT)
        occ = set(self.snake.body)
        self.food = _empty_cell(self.rng, self.width, self.height, occ)

    def set_direction(self, direction: Direction) -> None:
        self.pending_direction = direction

    def step(self) -> None:
        if self.game_over:
            return
        nd = self.pending_direction
        if opposite(nd, self.snake.direction):
            nd = self.snake.direction
        new_head = next_cell(self.snake.head(), nd)

        if new_head[0] < 0 or new_head[0] >= self.height or new_head[1] < 0 or new_head[1] >= self.width:
            self.game_over = True
            return

        if new_head in self.snake.body[:-1]:
            self.game_over = True
            return

        eat = new_head == self.food
        self.snake.advance(nd, eat=eat)
        if eat:
            self.score += POINTS_PER_FOOD
            occ = set(self.snake.body)
            self.food = _empty_cell(self.rng, self.width, self.height, occ)
