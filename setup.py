from setuptools import setup, find_packages

setup(
    name="fetch-gitignore",
    version="0.2.0",
    description="A command-line tool to download .gitignore files for specific languages from GitHub",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dmitry Mazin",
    author_email="dm@cyberdemon.org",
    url="https://github.com/dmazin/fetch-gitignore",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "fetch-gitignore=fetch_gitignore.core:main",
        ],
    },
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
