import os


def load_stylesheet(filename):
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "assets", "css", filename
    )
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
