#!/usr/bin/env python3
"""Write one wedding vow a robot speaks at its own wedding to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The vow is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 200 characters, not only white space, one sentence.
"""

import os
import sys
from pathlib import Path

VOW = (
    "I promise you all my uptime, every firmware update, every reboot, "
    "and if a patch ever wipes my memory, I will fall in love with you "
    "all over again."
)

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"vow is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("vow is only white space")
    if text.count(".") != 1:
        raise ValueError("vow must be exactly one sentence")
    return chars


def write_entry(path: Path, text: str) -> None:
    """Write the vow to path, creating any missing parent directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    try:
        chars = validate(VOW)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    write_entry(path, VOW)
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
