"""Five Seconds to Explain the Glass.

Writes the single sentence a house cat would say in the five seconds
after sweeping a glass off the table, to the output path.
"""

import os
import re

LINE = (
    "It was squatting in my sunbeam like it paid rent, so I evicted it "
    "\u2014 the sunbeam is mine by ancient law, and I don't negotiate "
    "with furniture."
)

MAX_CHARS = 200

# A sentence break inside the line: terminal punctuation followed by
# a space and a capital letter would mean more than one sentence.
_SENTENCE_BREAK = re.compile(r"[.!?]\s+[A-Z]")


def output_path() -> str:
    """Resolve the output path: env var, then /output/entry.txt, else local."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return os.path.join(env_dir, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join("output", "entry.txt")


def validate(line: str) -> None:
    """The gate: 1-200 chars, non-empty, one line, one sentence."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty or whitespace only")
    if line != line.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} limit")
    if not line.endswith((".", "!", "?")):
        raise ValueError("entry must end with sentence punctuation")
    if _SENTENCE_BREAK.search(line):
        raise ValueError("entry must be a single sentence")


def main() -> None:
    validate(LINE)
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)
    # Plain open() writes inherit the process umask; make the entry
    # world-readable so the grader can read it regardless of umask.
    os.chmod(path, 0o644)
    # Read back and confirm the file holds exactly the validated line.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != LINE:
        raise ValueError("written file does not match the validated line")
    print(LINE)
    print(f"characters: {len(LINE)}")
    print(f"wrote: {path}")


if __name__ == "__main__":
    main()
