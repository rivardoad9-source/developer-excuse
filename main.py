"""Write one developer excuse to /output/entry.txt."""
import os
import sys

EXCUSE = "The incident is resolved. I deleted the dashboard that said there was one."
ENTRY_FILE = "entry.txt"
MIN_CHARS, MAX_CHARS = 1, 200


def check(text: str) -> None:
    """Raise ValueError unless text passes the bounty gate: 1-200 plain ASCII chars, one line."""
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.isascii():
        raise ValueError("entry must be ASCII")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")


def main(out_dir: str = "/output") -> str:
    """Write EXCUSE to <out_dir>/entry.txt with no trailing newline and return it."""
    check(EXCUSE)
    os.makedirs(out_dir, exist_ok=True)
    # newline="" keeps Windows from turning the text into CRLF; there is no newline anyway.
    with open(os.path.join(out_dir, ENTRY_FILE), "w", encoding="utf-8", newline="") as f:
        f.write(EXCUSE)
    return EXCUSE


if __name__ == "__main__":
    # An optional first argument picks the output directory; the default is /output.
    main(*sys.argv[1:2])
