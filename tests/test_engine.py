# DAG owner: tester
from __future__ import annotations

import random

from config.settings import POINTS_PER_FOOD
from game.engine import GameEngine
from game.snake import Direction


def test_score_on_food() -> None:
    eng = GameEngine(rng=random.Random(42))
    hr, hc = eng.snake.head()
    eng.food = (hr, hc + 1)
    eng.set_direction(Direction.RIGHT)
    eng.step()
    assert eng.score == POINTS_PER_FOOD


def test_wall_collision() -> None:
    eng = GameEngine(rng=random.Random(1))
    eng.snake.body = [(0, 0)]
    eng.snake.direction = Direction.UP
    eng.set_direction(Direction.UP)
    eng.step()
    assert eng.game_over
