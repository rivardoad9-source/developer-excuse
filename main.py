"""Write one developer excuse to /output/entry.txt."""
import os

EXCUSE = "The incident is resolved. I deleted the dashboard that said there was one."
ENTRY_FILE = "entry.txt"


def main(out_dir: str = "/output") -> str:
    """Write EXCUSE to <out_dir>/entry.txt with no trailing newline and return it."""
    os.makedirs(out_dir, exist_ok=True)
    # newline="" keeps Windows from turning the text into CRLF; there is no newline anyway.
    with open(os.path.join(out_dir, ENTRY_FILE), "w", encoding="utf-8", newline="") as f:
        f.write(EXCUSE)
    return EXCUSE


if __name__ == "__main__":
    main()
