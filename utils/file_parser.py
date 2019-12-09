from pathlib import Path


def get_lines_from_path(path):
    f = Path(path)
    return f.read_text().split("\n")
