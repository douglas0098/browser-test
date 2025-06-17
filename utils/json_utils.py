import json
import os

TRANSLATION_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "config", "translations.json"
)


def load_translations():
    with open(TRANSLATION_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_language_names():
    with open(TRANSLATION_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
