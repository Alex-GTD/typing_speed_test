# texts.py
from .config import resource_path

def load_words():
    """Load words from a text file, stripping whitespace and ignoring empty lines"""
    path = "app/data/words.txt"
    real_path = resource_path(path)
    with open(real_path, encoding="utf-8") as f:
        return [w.strip() for w in f if w.strip()]
