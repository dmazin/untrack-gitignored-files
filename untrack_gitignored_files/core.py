import os
import argparse
import fnmatch
from git.repo import Repo


def read_gitignore(repo):
    gitignore_path = os.path.join(repo.working_dir, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as gitignore_file:
            return gitignore_file.read().splitlines()
    else:
        return []


def list_tracked_gitignored_files(repo, gitignore_patterns):
    tracked_gitignored_files = []

    for file in repo.index.entries.keys():
        file_path = file[0]
        for pattern in gitignore_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                tracked_gitignored_files.append(file)

    return tracked_gitignored_files


def untrack_gitignored_files(repo, gitignore_patterns) -> int:
    tracked_gitignored_files = list_tracked_gitignored_files(repo, gitignore_patterns)
    if not tracked_gitignored_files:
        print("No tracked gitignored files found.")
        return 0

    for file_tuple in tracked_gitignored_files:
        file_path = file_tuple[0]
        repo.index.remove([file_path], working_tree=True)
        print(f"Untracked {file_path}.")

    return len(tracked_gitignored_files)


def main():
    parser = argparse.ArgumentParser(description="Untrack gitignored files.")
    parser.add_argument(
        "--doit",
        action="store_true",
        help="Actually untrack gitignored files.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Create a commit after untracking files.",
    )

    args = parser.parse_args()

    repo = Repo(".")

    gitignore_patterns = read_gitignore(repo)

    tracked_gitignored_files = list_tracked_gitignored_files(repo, gitignore_patterns)
    if tracked_gitignored_files:
        print("Tracked gitignored files:")
        for file in tracked_gitignored_files:
            print(f"{file[0]}")

        if args.doit:
            num_files_untracked: int = untrack_gitignored_files(
                repo, gitignore_patterns
            )
            if args.commit and num_files_untracked > 0:
                repo.index.commit("Untracked gitignored files.")
    else:
        print("No tracked gitignored files found.")


if __name__ == "__main__":
    main()
