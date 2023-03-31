import os
import sys
import requests
import argparse
import fnmatch
from git.repo import Repo


def fetch_gitignore(repo, language):
    base_url = "https://raw.githubusercontent.com/github/gitignore/master/"
    file_name = f"{language}.gitignore"

    response = requests.get(base_url + file_name)

    if response.status_code == 200:
        with open(".gitignore", "w") as gitignore_file:
            gitignore_file.write(response.text)
        print(f"Downloaded {language} .gitignore successfully.")
        return response.text.splitlines()
    else:
        print(f"Error: {language} .gitignore not found.")
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
    parser = argparse.ArgumentParser(
        description="Fetch .gitignore, optionally untracking gitignored files."
    )
    parser.add_argument("language", help="Language for .gitignore")
    parser.add_argument(
        "--untrack-gitignored-files",
        action="store_true",
        help="Untrack gitignored files",
    )
    parser.add_argument(
        "--replace", action="store_true", help="Replace existing .gitignore file."
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Create a commit after downloading .gitignore, and after untracking files.",
    )

    args = parser.parse_args()

    if os.path.exists(".gitignore") and not args.replace:
        print(".gitignore already exists. Use --replace to overwrite.")
        sys.exit(1)

    repo = Repo(".")

    gitignore_patterns = fetch_gitignore(repo, args.language)
    if args.commit:
        repo.index.commit("Added .gitignore for {args.language}.")

    if args.untrack_gitignored_files:
        num_files_untracked: int = untrack_gitignored_files(repo, gitignore_patterns)
        if args.commit and num_files_untracked > 0:
            repo.index.commit("Untracked gitignored files.")
    else:
        tracked_gitignored_files = list_tracked_gitignored_files(
            repo, gitignore_patterns
        )
        if tracked_gitignored_files:
            print("Tracked gitignored files:")
            for file in tracked_gitignored_files:
                print(f"{file[0]}")
        else:
            print("No tracked gitignored files found.")


if __name__ == "__main__":
    main()
