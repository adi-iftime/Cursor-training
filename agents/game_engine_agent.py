"""
Game Engine Agent — owns snake movement, collisions, tick/step, in-session scoring.

Implementation modules: `game/snake.py`, `game/engine.py`.
"""

from __future__ import annotations

from game.engine import GameEngine
from game.snake import Direction, Snake, next_cell, opposite

__all__ = ["GameEngine", "Direction", "Snake", "next_cell", "opposite"]
