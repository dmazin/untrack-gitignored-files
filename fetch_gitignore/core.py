import sys
import requests
import argparse
import fnmatch
from git import Repo


def fetch_gitignore(language):
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
        for pattern in gitignore_patterns:
            if fnmatch.fnmatch(file, pattern):
                tracked_gitignored_files.append(file)

    return tracked_gitignored_files


def untrack_gitignored_files(repo, gitignore_patterns):
    tracked_gitignored_files = list_tracked_gitignored_files(repo, gitignore_patterns)
    if not tracked_gitignored_files:
        print("No files to untrack.")
        return

    for file in tracked_gitignored_files:
        repo.index.remove([file], working_tree=True)
        print(f"Untracked {file}.")

    repo.index.commit("Untracked gitignored files.")


def main():
    parser = argparse.ArgumentParser(description="Fetch and handle .gitignore")
    parser.add_argument("language", help="Language for .gitignore")
    parser.add_argument(
        "--untrack-gitignored-files",
        action="store_true",
        help="Untrack gitignored files",
    )

    args = parser.parse_args()

    gitignore_patterns = fetch_gitignore(args.language)

    repo = Repo(".")

    if args.untrack_gitignored_files:
        untrack_gitignored_files(repo, gitignore_patterns)
    else:
        tracked_gitignored_files = list_tracked_gitignored_files(repo, gitignore_patterns)
        if tracked_gitignored_files:
            print("Tracked gitignored files:")
            for file in tracked_gitignored_files:
                print(f"  {file}")
        else:
            print("No tracked gitignored files found.")


if __name__ == "__main__":
    main()
