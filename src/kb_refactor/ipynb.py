import json
from pathlib import Path
import re
import os
from typing import Any, Match

INLINE_CODE_RE = re.compile(r'`[^`\n]+`')
FENCED_CODE_RE = re.compile(r'```.*?```', re.DOTALL)


def make_relative(src: Path, target: Path):
    return os.path.relpath(
        target,
        start=src.parent,
    ).replace('\\', '/')


def protect(text: str):
    protected = []

    def repl(match: Match[str]):
        token: str = f'__PROTECTED_{len(protected)}__'
        protected.append(match.group(0))
        return token

    text = FENCED_CODE_RE.sub(repl, text)
    text = INLINE_CODE_RE.sub(repl, text)

    return text, protected


def restore(txt, protected):
    for i, val in enumerate(protected):
        txt = txt.replace(
            f'__PROTECTED_{i}__',
            val,
        )

    return txt


def process_markdown(
    text: str,
    ipynb_path: Path,
    idx: dict[str, Path],
):
    text, protected = protect(text)

    kbids = sorted(
        idx.keys(),
        key=len,
        reverse=True,
    )

    pattern = re.compile(
        r'(?<![\w])('
        + '|'.join(
            map(re.escape, kbids)
        )
        + r')(?![\w])'
    )

    def repl(match):
        kbid = match.group(1)

        rel = make_relative(
            ipynb_path,
            idx[kbid],
        )

        return f'[{kbid}]({rel})'

    text = pattern.sub(repl, text)

    text = restore(text, protected)

    return text


def process_ipynb(
    ipynb_path: Path,
    idx: dict[str, Path],
) -> tuple[Any, bool]:
    with ipynb_path.open(
        'r',
        encoding='utf-8',
    ) as f:
        ipynb = json.load(f)

    changed = False

    for cell in ipynb.get('cells', []):

        if cell.get('cell_type') != 'markdown':
            continue

        source = ''.join(
            cell.get('source', [])
        )

        updated = process_markdown(
            source,
            ipynb_path,
            idx,
        )

        if updated != source:
            changed = True
            cell['source'] = updated.splitlines(
                keepends=True
            )

    return ipynb, changed