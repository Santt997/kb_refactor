from pathlib import Path
import json
import sys

EXCLUDED_DIRS : set[str] = {
    '.git',
    '.ipynb_checkpoints',
    '__pycache__',
    '.venv',
    'venv',
    'env',
}


def iter_ipynbs(root: Path):
    for path in root.rglob('*.ipynb'):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        yield path


def load_notebook(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def build_index(root: Path) -> dict[str, Path]:
    idx : dict[str, Path] = {}

    for nb_path in iter_ipynbs(root):

        nb = load_notebook(nb_path)

        kbid = nb.get('metadata', {}).get('kbId')

        if not kbid:
            continue

        if kbid in idx:
            print(
                f'ERROR duplicated kbId: {kbid}',
                file=sys.stderr,
            )
            sys.exit(1)

        idx[kbid] = nb_path

    return idx