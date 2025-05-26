# config.py
import sys
import os

# ====== Paths ======
# Project root — the directory where main.py is located
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR     = os.path.join(PROJECT_ROOT, "app", "data")
HIGH_SCORE_FILE = os.path.join(DATA_DIR, "high_score.txt")

# ====== Colors & Fonts ======
# Dark theme color palette
BG_COLOR = "#121212"
WIDGET_BG = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#03DAC6"

FONT_NORMAL = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")

# ====== Settings ======
# Core application parameters
INITIAL_TIME = 60 # Initial countdown duration in seconds
CANVAS_WIDTH = 500 # Main canvas dimensions
CANVAS_HEIGHT = 300

def resource_path(relative_path):
    """Возвращает абсолютный путь к ресурсу, работает и в .exe и в IDE"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
