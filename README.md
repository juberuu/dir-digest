# dir-digest

A small command-line tool that prints a readable summary of a directory: file counts, sizes, and a compact tree.

## Usage

```bash
python dir_digest.py .
python dir_digest.py . --json
python dir_digest.py . --max-depth 2 --ignore .git --ignore __pycache__
```

## Requirements

Python 3.10 or newer. No third-party packages.
