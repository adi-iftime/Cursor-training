"""Curses presentation + input loop (Integration Agent wires this to CLI)."""

from __future__ import annotations

import curses

from game.engine import GameEngine
from game.snake import Direction


def _draw(stdscr: curses.window, engine: GameEngine) -> None:
    stdscr.erase()
    h, w = engine.height, engine.width
    for r in range(h + 2):
        row: list[str] = []
        for c in range(w + 2):
            if r == 0 or r == h + 1 or c == 0 or c == w + 1:
                row.append("#")
            else:
                rr, cc = r - 1, c - 1
                cell = (rr, cc)
                if cell == engine.snake.head():
                    row.append("@")
                elif cell in engine.snake.body[1:]:
                    row.append("o")
                elif cell == engine.food:
                    row.append("*")
                else:
                    row.append(".")
        stdscr.addstr(r, 0, "".join(row))
    stdscr.addstr(h + 2, 0, f"Score: {engine.score}  |  Arrows move  Q quit")
    stdscr.refresh()


def run_play_session() -> int:
    """Run one game session; return final score."""
    engine = GameEngine()

    def _run(stdscr: curses.window) -> int:
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(120)
        _draw(stdscr, engine)
        while not engine.game_over:
            key = stdscr.getch()
            if key in (ord("q"), ord("Q")):
                break
            if key == curses.KEY_UP:
                engine.set_direction(Direction.UP)
            elif key == curses.KEY_DOWN:
                engine.set_direction(Direction.DOWN)
            elif key == curses.KEY_LEFT:
                engine.set_direction(Direction.LEFT)
            elif key == curses.KEY_RIGHT:
                engine.set_direction(Direction.RIGHT)
            engine.step()
            _draw(stdscr, engine)
        return engine.score

    return int(curses.wrapper(_run))
