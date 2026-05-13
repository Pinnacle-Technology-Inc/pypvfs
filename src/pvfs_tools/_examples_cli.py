"""Entry point for the ``pypvfs-examples`` console script.

Prints the on-disk location of the examples shipped inside the installed
package and, optionally, copies them out to a user-chosen directory so they
can be edited freely. This is the discoverable counterpart to::

    python -m pvfs_tools.examples.pvfs_create_cli ...
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def _examples_dir() -> Path:
    return Path(__file__).parent / "examples"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pypvfs-examples",
        description=(
            "Locate or copy out the runnable example scripts that ship with "
            "pypvfs (PVFS-to-EDF, PVFS-to-WebM, synthetic PVFS creation)."
        ),
    )
    parser.add_argument(
        "--copy-to",
        type=Path,
        metavar="DIR",
        help="Copy every example .py file into DIR (created if missing) "
        "so you can edit them in place.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the names of bundled example modules.",
    )
    args = parser.parse_args(argv)

    src = _examples_dir()
    if not src.is_dir():
        print(
            "pypvfs-examples: bundled examples directory not found at "
            f"{src}. This usually means pypvfs was installed from a wheel "
            "built before examples were bundled; try `pip install --upgrade "
            "pypvfs`.",
            file=sys.stderr,
        )
        return 1

    print(f"Bundled examples live at: {src}")

    scripts = sorted(p for p in src.glob("*.py") if p.name != "__init__.py")
    if args.list or not args.copy_to:
        print("\nAvailable example modules:")
        for p in scripts:
            mod = f"pvfs_tools.examples.{p.stem}"
            print(f"  python -m {mod}")

    if args.copy_to is not None:
        dest = args.copy_to.expanduser().resolve()
        dest.mkdir(parents=True, exist_ok=True)
        for p in scripts:
            target = dest / p.name
            shutil.copy2(p, target)
            print(f"copied {p.name} -> {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
