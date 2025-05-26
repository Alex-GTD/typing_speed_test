# storage.py
import os
from .config import DATA_DIR, HIGH_SCORE_FILE


def ensure_data_dir():
    """Ensure the data directory exists, create it if necessary"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def get_high_score():
    """Retrieve the current high score from persistent storage

    Returns:
        int: The highest score recorded (0 if no record exists or file is corrupted)
    """
    ensure_data_dir()
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            # Attempt to read and parse the high score file
            return int(open(HIGH_SCORE_FILE).read())
        except ValueError:
            # Handle case where file contains invalid data
            return 0
    return 0  # Default value if no record exists


def save_high_score_if_beaten(new_score):
    """Update high score if the new score beats the current record

    Args:
        new_score (int): The score to potentially save as new high score

    Returns:
        int: The current high score (whether updated or not)
    """
    ensure_data_dir()
    high_score = get_high_score()
    if new_score > high_score:
        # Atomic write operation for high score persistence
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(new_score))
        return new_score
    return high_score