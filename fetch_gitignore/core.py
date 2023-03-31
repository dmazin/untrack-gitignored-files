import sys
import requests

def fetch_gitignore(language):
    base_url = "https://raw.githubusercontent.com/github/gitignore/master/"
    file_name = f"{language}.gitignore"

    response = requests.get(base_url + file_name)

    if response.status_code == 200:
        with open(".gitignore", "w") as gitignore_file:
            gitignore_file.write(response.text)
        print(f"Downloaded {language} .gitignore successfully.")
    else:
        print(f"Error: {language} .gitignore not found.")

def main():
    if len(sys.argv) > 1:
        language = sys.argv[1]
        fetch_gitignore(language)
    else:
        print("Usage: fetch-gitignore <language>")

