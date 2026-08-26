"""Webots launch helpers for Maze Graph Memory Bot."""

from __future__ import annotations

from dataclasses import asdict
import os
from pathlib import Path
import shutil
from typing import Any
import sys


APP_DIR = Path(__file__).resolve().parent
CGF_ROOT = APP_DIR.parents[1]
BOTS_DIR = CGF_ROOT / "applications" / "bots"
WORLD_PATH = APP_DIR / "main" / "worlds" / "maze_graph_memory.wbt"

if str(BOTS_DIR) not in sys.path:
    sys.path.insert(0, str(BOTS_DIR))

from graph_memory_bot import run_graph_memory_bot_demo  # noqa: E402


def webots_world_path() -> Path:
    return WORLD_PATH


def _find_webots_executable() -> str | None:
    webots_home = os.environ.get("WEBOTS_HOME")
    if webots_home:
        candidate = Path(webots_home) / "msys64" / "mingw64" / "bin" / "webots.exe"
        if candidate.exists():
            return str(candidate)
        candidate = Path(webots_home) / "webots.exe"
        if candidate.exists():
            return str(candidate)
    return shutil.which("webots")


def build_webots_launch_info(seed: int = 0, max_ticks: int = 60) -> dict[str, Any]:
    executable = _find_webots_executable()
    command = None
    if executable:
        command = [executable, "--mode=fast", str(WORLD_PATH)]
    return {
        "app": "Maze Graph Memory Bot",
        "world": str(WORLD_PATH),
        "controller": "maze_graph_memory_controller",
        "seed": seed,
        "max_ticks": max_ticks,
        "webots_executable": executable,
        "command": command,
        "claim": "Webots graph-action fixture only",
    }


def run_webots_app(seed: int = 0, max_ticks: int = 60) -> dict[str, Any]:
    if not WORLD_PATH.exists():
        return {
            "status": "skipped",
            "reason": "missing_webots_world",
            "world": str(WORLD_PATH),
        }
    info = build_webots_launch_info(seed=seed, max_ticks=max_ticks)
    if info["webots_executable"] is None:
        return {
            "status": "skipped",
            "reason": "missing_webots_executable",
            **info,
        }
    return {
        "status": "available",
        "reason": "webots_executable_found",
        **info,
    }


def build_graph_memory_trace(seed: int = 0, max_ticks: int = 3) -> dict[str, Any]:
    run = run_graph_memory_bot_demo(seed=seed, max_ticks=max_ticks)
    return asdict(run)


if __name__ == "__main__":
    print(run_webots_app())
