"""Game Engine Agent — scoring and collision invariants."""

from __future__ import annotations

import random

from config.settings import POINTS_PER_FOOD
from game.engine import GameEngine
from game.snake import Direction


def test_score_increases_when_food_eaten() -> None:
    rng = random.Random(42)
    eng = GameEngine(rng=rng)
    hr, hc = eng.snake.head()
    eng.food = (hr, hc + 1)
    eng.set_direction(Direction.RIGHT)
    eng.step()
    assert eng.score == POINTS_PER_FOOD
    assert eng.food != eng.snake.head()


def test_wall_collision_ends_game() -> None:
    eng = GameEngine(rng=random.Random(1))
    eng.snake.body = [(0, 0)]
    eng.snake.direction = Direction.UP
    eng.set_direction(Direction.UP)
    eng.step()
    assert eng.game_over


def test_opposite_input_ignored_for_move() -> None:
    eng = GameEngine(rng=random.Random(0))
    eng.set_direction(Direction.LEFT)
    eng.step()
    assert not eng.game_over
