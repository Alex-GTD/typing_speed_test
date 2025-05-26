# logic.py
import random
from .texts import load_words

def get_shuffled_words():
    # Load words and shuffle them for the typing test
    words_list = load_words()
    random.shuffle(words_list)
    return words_list, " ".join(words_list)

def calculate_score(typed_words, words_list):
    # Compares typed words against original list, returns correct count
    # Note: Only counts sequentially matching words (stops at first mismatch)
    score = 0
    target = 0
    for tw in typed_words:
        if target < len(words_list) and tw == words_list[target]:
            score += 1
            target += 1
    return score

def color_text(entry, words_list):
    # Reset all text coloring before reprocessing
    entry.tag_remove("correct", "1.0", "end")
    entry.tag_remove("incorrect", "1.0", "end")

    # Color each word green if it exists in remaining words, red otherwise
    full_text = entry.get("1.0", "end-1c")
    remaining = words_list.copy()  # Working copy to track remaining valid words
    idx = 0
    for word in full_text.split():
        start = f"1.{idx}"
        end   = f"1.{idx + len(word)}"
        if word in remaining:
            entry.tag_add("correct", start, end)
            remaining.remove(word)  # Each correct word can only be used once
        else:
            entry.tag_add("incorrect", start, end)
        idx += len(word) + 1  # +1 for the space after each word

    # Configure tag colors (green for correct, red for incorrect)
    entry.tag_config("correct",   foreground="green")
    entry.tag_config("incorrect", foreground="red")