#!/usr/bin/python3
"""
Wrapper for running linters on entire git repo.
Tested on Ubuntu
"""
import argparse
import glob
import os
import re
import subprocess
import sys

from itertools import chain
from os import path
from typing import Iterator, List, Dict

DEBUG = 0


LINTERS = {
    "c": {
        "extensions": ["c", "h"],
        "program": "clang-format-9",
        "excludes": "config/c-exclude.txt",
        "args": ["-i", "-style=file", "-fallback-style=none"],
    },
    "python": {
        "extensions": ["py"],
        "program": "black",
        "args": ["-l", "100"],
        "exclude": "config/py-exclude.txt",
    },
    "docker": {
        "extensions": [None],
        "nameFilter": "Dockerfile",
        "program": "hadolint",
        "excludes": "config/docker-exclude.txt",
    },
}


def read_exclusions(fileconfig: str = None) -> List[str]:
    """
    Reads the provided exclusion configuration file and returns a list of files to exclude from lint.
    """
    res = set()
    if fileconfig and path.exists(fileconfig):
        with open(fileconfig, "r") as fr:
            for line in fr:
                if line.strip():
                    res.add(line.strip())
    return list(res)


def find_files(
    dir: str = ".",
    extensions: List[str] = [],
    exclude: List[str] = [],
    include: List[str] = [],
    nameFilter: str = None,
    recursive: bool = True,
) -> List[str]:
    """
    Finds all the files at base directory that match the provided extension list, excluding any file that matches an entry of the exclude list.
    If recursive is True, will search all paths below base. Otherwise will only lint files immediately in directory
    """
    # Transform exlucde string list to regex list for search
    excl = []
    for e in exclude:
        excl.append(re.compile(e.replace(".", "\.").replace("*", ".*")))

    # Create search string that should find all files in the location
    search = ""
    if dir != "." and dir != "./":
        if dir[-1] != "/":
            dir += "/"
        search += dir
    if recursive:
        search += "**/"
    if nameFilter:
        search += nameFilter
    else:
        search += "*"

    if DEBUG:
        print(search)
    # Search for all filetypes and return an Iterator
    tmp = []
    for e in extensions:
        if e is None:
            tmp.append(glob.iglob(search, recursive=recursive))
        else:
            tmp.append(glob.iglob(search + ".%s" % e, recursive=recursive))

    # remove any exluded file
    res = []
    for filename in chain(*tmp):
        store = True
        for exclRe in excl:
            if exclRe.fullMatch(filename):
                store = False
                break
        # filter on includes list only if it exists
        if include is not None and filename not in include:
            store = False
        if store:
            res.append(filename)

    return res


def run_linter(
    program: str, filelist: List[str], args: List[str] = [], successRc: int = 0
) -> Dict[str, str]:
    """
    Runs the specific program with the provdied args on all files in filelist.

    """
    res = {}
    for filename in filelist:
        cmd = [program]
        cmd += args
        cmd.append(filename)
        if DEBUG:
            print(cmd)
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        # Check returncode
        if result.returncode != successRc:
            res[filename] = result.stdout.decode("utf-8").split("\n")
    return res


def git_diff_results(dir: str) -> List[str]:
    """
    Runs a git diff and returns a list of files that have been modified.
    """
    cmd = ["git", "diff", "--name-only"]
    # Has to be executed inside the git directory - save cur dir to switch back to.
    curr = os.getcwd()
    os.chdir(dir)
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    os.chdir(curr)
    if result.returncode != 0:
        return []
    return result.stdout.decode("utf-8").split("\n")


def main(dir: str = ".", recursive: bool = True, diffOnly: bool = False) -> int:
    """
    Runs all linters and modifies files in place (if supported)
    To add a linter, add it's configuration in LINTER map at the start of the module.
    """
    res = {}
    fstr = "Local"
    if recursive:
        fstr = "All"
    include = None
    if diffOnly:
        include = git_diff_results(dir)
    for language in LINTERS:
        # These must be included in linter congifurations
        program = LINTERS[language]["program"]
        print("Running %s on %s %s files in %s." % (program, fstr, language, dir))
        # Check all optional params and default to standard values
        extensions = LINTERS[language].get("extensions", [None])
        excludeFile = LINTERS[language].get("excludes", None)
        args = LINTERS[language].get("args", [])
        nameFilter = LINTERS[language].get("nameFilter", None)
        # Build exclusion list from config file and then find all matching files
        exclude = read_exclusions(excludeFile)
        filelist = find_files(
            dir=dir,
            extensions=extensions,
            exclude=exclude,
            include=include,
            recursive=recursive,
            nameFilter=nameFilter,
        )
        if DEBUG:
            print(filelist)
        res.update(run_linter(program, filelist, args))
    # 0 is success, means no files were modified
    if res:
        print(res)
    return len(res.keys())


if __name__ == "__main__":
    # Parse provided args
    parser = argparse.ArgumentParser(description="Wrapper for running lint on any filetype.")
    parser.add_argument("-d", "--dir", type=str, default=".", help="Directory to run linter on.")
    parser.add_argument(
        "-g",
        "--git",
        action="store_true",
        help="Flag to indicate this is a git commit linter run and should only check files that have been modified before commit.",
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recursively search for files below dir.",
    )
    args = parser.parse_args()
    # Run and exit with success/error based on number of linted files
    sys.exit(main(dir=args.dir, recursive=args.recursive, diffOnly=args.git))
