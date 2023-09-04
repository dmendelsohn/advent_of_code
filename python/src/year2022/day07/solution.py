import re
from typing import Optional


class Command:
    @staticmethod
    def parse(text: str) -> "Command":
        if text.startswith("cd"):
            return Cd.parse(text)
        elif text.startswith("ls"):
            return Ls.parse(text)
        else:
            raise ValueError(f"Could not parse: {text}")


class Cd(Command):
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return f"Cd(arg={self.arg})"

    @staticmethod
    def parse(text: str) -> "Cd":
        match = re.match("cd (.*)", text.strip())
        if not match:
            raise ValueError(f"Could not parse: {text}")

        return Cd(match.groups()[0])


class Ls(Command):
    def __init__(self, files: dict[str, int], directories: set[str]):
        self.files = files
        self.directories = directories

    def __repr__(self):
        return f"Cd(files={self.files}, directories={self.directories})"

    @staticmethod
    def parse(text: str) -> "Ls":
        lines = text.strip().split("\n")
        if not lines or lines[0] != "ls":
            raise ValueError(f"Could not parse: {text}")

        files = {}
        directories = set()
        for line in lines[1:]:
            match = re.match(r"dir (.*)", line)
            if match:
                directories.add(match.groups()[0])
                continue
            match = re.match(r"(\d+) (.*)", line)
            if match:
                filesize, filename = match.groups()
                files[filename] = int(filesize)
                continue

            raise ValueError(f"Could not parse {line=}")

        return Ls(files, directories)


def parse_input(text: str) -> list[Command]:
    return [Command.parse(command) for command in text.lstrip("$ ").split("$ ")]


class Directory:
    def __init__(self, parent: Optional["Directory"] = None):
        self.parent = parent
        self.files: dict[str, int] = {}
        self.directories: dict[str, Directory] = {}

    def add(self, ls: Ls) -> None:
        self.files.update(ls.files)
        for directory_name in ls.directories:
            if directory_name not in self.directories:
                self.directories[directory_name] = Directory(parent=self)

    def recursive_get_size(self) -> dict[tuple, int]:
        result = {}

        total_size = 0
        for directory_name, directory in self.directories.items():
            for sub_path, size in directory.recursive_get_size().items():
                if not sub_path:
                    # This is the immediate subdirectory
                    total_size += size
                result[(directory_name, *sub_path)] = size

        for filesize in self.files.values():
            total_size += filesize

        result[tuple()] = total_size
        return result

    def __repr__(self) -> str:
        return f"Directory(files={self.files}, directories={self.directories})"


def build_filesystem(commands: list[Command]) -> Directory:
    """Build a filesystem based on the commands and return the root directory"""
    root = cwd = Directory()
    for command in commands:
        if isinstance(command, Cd):
            if command.arg == "/":
                cwd = root
            elif command.arg == "..":
                if cwd.parent is None:
                    raise RuntimeError("Cannot navigate to parent of the root directory")
                cwd = cwd.parent
            else:
                cwd = cwd.directories[command.arg]
            pass
        elif isinstance(command, Ls):
            cwd.add(command)
        else:
            raise ValueError(f"Unrecognized command: {command}")
    return root


def part_1(puzzle_input: str) -> str | int:
    commands = parse_input(puzzle_input)
    root = build_filesystem(commands)
    return sum(size for size in root.recursive_get_size().values() if size <= 10**5)


def part_2(puzzle_input: str) -> str | int:
    commands = parse_input(puzzle_input)
    root = build_filesystem(commands)
    sizes = root.recursive_get_size()
    space_to_free = sizes[tuple()] - 40_000_000
    return min(size for size in sizes.values() if size >= space_to_free)
