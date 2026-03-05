# cli.py
import shlex

from mini_git import (
    CommitGraph, InvertedIndex,
    merge_sort, find_path, find_ancestors,
)


def main():
    graph = None
    index = InvertedIndex()

    while True:
        try:
            line = input("mini-git> ")
        except EOFError:
            break

        line = line.strip()
        if not line:
            continue

        try:
            tokens = shlex.split(line)
        except ValueError:
            tokens = line.split()

        if not tokens:
            continue

        cmd = tokens[0].upper()

        if cmd in ("EXIT", "QUIT"):
            break

        elif cmd == "INIT":
            if len(tokens) < 2:
                print("(error) ERR wrong number of arguments")
                continue
            pass  # TODO

        elif cmd == "COMMIT":
            if len(tokens) < 2:
                print("(error) ERR wrong number of arguments")
                continue
            pass  # TODO

        elif cmd == "BRANCH":
            if len(tokens) < 2:
                print("(error) ERR wrong number of arguments")
                continue
            pass  # TODO

        elif cmd == "SWITCH":
            if len(tokens) < 2:
                print("(error) ERR wrong number of arguments")
                continue
            pass  # TODO

        elif cmd == "LOG":
            pass  # TODO

        elif cmd == "PATH":
            if len(tokens) < 3:
                print("(error) ERR wrong number of arguments")
                continue
            pass  # TODO

        elif cmd == "ANCESTORS":
            if len(tokens) < 2:
                print("(error) ERR wrong number of arguments")
                continue
            pass  # TODO

        elif cmd == "SEARCH":
            if len(tokens) < 2:
                print("(error) ERR wrong number of arguments")
                continue
            pass  # TODO

        else:
            print(f"(error) ERR unknown command '{tokens[0]}'")


if __name__ == "__main__":
    main()
