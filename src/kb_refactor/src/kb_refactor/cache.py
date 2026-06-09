import json
from pathlib import Path
from typing import Any

CACHE_FILE : str = '.kb_refactor_cache.json'
CACHE_VERSION : int = 2


def cache_path(root: Path) -> Path:
    return root / CACHE_FILE


def load_cache(root: Path) -> dict[str, Any] | None:
    path : Path = cache_path(root)

    if not path.exists():
        return None

    try:
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        if data.get('version') != CACHE_VERSION:
            return None

        return data

    except Exception:
        return None


def save_cache(root: Path, data: dict[str, Any]) -> None:
    path : Path = cache_path(root)

    with path.open('w', encoding='utf-8') as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )
        f.write('\n')