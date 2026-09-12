from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class RepairAction:
    name: str
    reversible: bool
    run: Callable[[dict], str]

def recreate_nonsecret_folder(ctx: dict) -> str:
    path = Path(ctx["path"])
    path.mkdir(parents=True, exist_ok=True)
    return f"folder_present:{path}"

def clear_companion_cache(ctx: dict) -> str:
    path = Path(ctx["path"])
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        return "cache_absent_created"
    for child in path.iterdir():
        if child.is_file():
            child.unlink()
    return "cache_files_cleared"

REGISTRY = {
    "recreate_nonsecret_folder": RepairAction("recreate_nonsecret_folder", True, recreate_nonsecret_folder),
    "clear_companion_cache": RepairAction("clear_companion_cache", True, clear_companion_cache),
}

def run_safe_repair(name: str, ctx: dict) -> str:
    action = REGISTRY.get(name)
    if not action or not action.reversible:
        raise ValueError("repair_not_authorized")
    return action.run(ctx)
