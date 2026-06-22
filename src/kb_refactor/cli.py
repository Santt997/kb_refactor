import argparse
import json
from pathlib import Path

from kb_refactor.idx import (
    build_index,
    iter_ipynbs,
)

from kb_refactor.ipynb import (
    process_ipynb,
)

from kb_refactor.stats import Stats


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'root',
        nargs='?',
        default='.',
    )

    for flag in (
        'dry-run',
        'check',
        'verbose',
        'stats',
    ):
        parser.add_argument(
            f"--{flag}",
            action="store_true",
        )

    return parser.parse_args()


def save_ipynb(
    path: Path,
    ipynb: str,
):
    with path.open(
        'w',
        encoding='utf-8',
    ) as f:
        json.dump(
            ipynb,
            f,
            ensure_ascii=False,
            indent=1,
        )
        f.write('\n')


def main() -> None:

    args = parse_args()

    root = Path(args.root).resolve()

    stats = Stats()

    idx : dict[str, Path] = build_index(root)

    changed : int = 0

    for nb_path in iter_ipynbs(root):

        stats.ipynbs += 1

        ipynb, was_changed = process_ipynb(
            nb_path,
            idx,
        )

        if not was_changed:
            continue

        changed += 1

        if args.verbose:
            print(
                f'Updated: {nb_path}'
            )

        if (
            not args.dry_run
            and not args.check
        ):
            save_ipynb(
                nb_path,
                ipynb,
            )

    if args.check:
        raise SystemExit(
            1 if changed else 0
        )

    print(
        f'Updated nbs: {changed}'
    )

    if args.stats:
        stats.report()