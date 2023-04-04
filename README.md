# untrack-gitignored-files
Fetch .gitignore from https://github.com/github/gitignore, optionally untracking gitignored files.

## Installation

```bash
pip install untrack-gitignored-files
```

## Usage

```bash
positional arguments:
  language              Language for .gitignore

options:
  -h, --help            show this help message and exit
  --untrack-gitignored-files
                        Untrack gitignored files
  --replace             Replace existing .gitignore file.
  --commit              Create a commit after downloading .gitignore, and after untracking
                        files.
```
