# gui.py
from tkinter import Tk, Canvas, Text, Label, Button, messagebox
import random
from tkinter import PhotoImage
from .config import *
from .logic import get_shuffled_words, calculate_score, color_text
from .storage import get_high_score, save_high_score_if_beaten

# — Global application state —
words_list, words = get_shuffled_words()
time_left = INITIAL_TIME
running   = False

# — Create main window and widgets —
window = Tk()
window.title("Typing Speed Test: WELCOME!")
window.columnconfigure(0, weight=1)
window.configure(bg=BG_COLOR)
window.resizable(False, False)

# logo Tkinter
logo = PhotoImage(file=resource_path("app/assets/logo.png"))
window.iconphoto(False, logo)



# Main text display canvas
canvas = Canvas(
    window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
    bg=WIDGET_BG, highlightthickness=0, bd=2, relief="groove"
)
canvas.grid(column=0, row=0, padx=30, pady=30)
text_id = canvas.create_text(
    CANVAS_WIDTH//2, CANVAS_HEIGHT//2,
    text="Press 'Start' to begin",
    fill=TEXT_COLOR, font=FONT_NORMAL, width=CANVAS_WIDTH-50
)

# Text entry widget (initially disabled)
entry = Text(
    window, height=2, width=45,
    bg=WIDGET_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR
)
entry.grid(column=0, row=1, padx=30, pady=10, sticky="ne")
entry.config(state="disabled")

# Score and time display labels
label_record = Label(
    window, text=f"High Score = {get_high_score()}",
    fg=TEXT_COLOR, bg=WIDGET_BG, font=FONT_NORMAL
)
label_record.grid(column=0, row=0, padx=(40, 0), pady=(40, 0), sticky="nw")

label_time = Label(
    window, text=f"Time: {time_left:02d}",
    fg=ACCENT_COLOR, bg=WIDGET_BG, font=FONT_BOLD
)
label_time.grid(column=0, row=0, padx=(0, 40), pady=(40, 0), sticky="ne")

# Random typing tips display
tips = [
    "Tip: Keep your fingers on home row.",
    "Tip: Breathe steadily while typing.",
    "Tip: Focus on accuracy first, then speed.",
    "Tip: Use all ten fingers for best results.",
    "Tip: Take a short stretch break every minute."
]
tip_label = Label(
    window, text=random.choice(tips),
    fg="#8888aa", bg=BG_COLOR, font=("Segoe UI",10,"italic")
)
tip_label.grid(column=0, row=2, pady=(10,0))

# Control buttons
button_start = Button(window, text="Start", width=12)
button_pause = Button(window, text="Pause", width=12)
button_stop  = Button(window, text="Stop",  width=12)
for btn, r in [(button_start,1),(button_pause,2),(button_stop,3)]:
    btn.grid(column=0, row=r, padx=(30,10), pady=10, sticky="w")


# — Event handlers —
def clear_and_disable_entry():
    """Utility function to reset the text entry widget"""
    entry.config(state="normal"); entry.delete("1.0","end"); entry.config(state="disabled")

def update_timer():
    """Countdown timer handler - updates every second"""
    global time_left
    if running and time_left >= 0:
        label_time.config(text=f"Time: {time_left:02d}")
        color_text(entry, words_list)  # Update text coloring in real-time
        time_left -= 1
        window.after(1000, update_timer)  # Recursive call after 1 second
    elif time_left < 0:
        evaluate_text()  # Time's up - evaluate results

def start():
    """Start the typing test"""
    global running
    window.title("Typing Speed Test: START!")
    if not running:
        running = True
        tip_label.grid_remove()
        entry.config(state="normal"); entry.focus()  # Enable typing
        canvas.itemconfig(text_id, text=words)  # Display words to type
        update_timer()  # Start countdown

def pause():
    """Pause the current test"""
    global running
    running = False
    window.title("Typing Speed Test: PAUSE!")
    entry.config(state="disabled")  # Disable typing
    tip_label.config(text=random.choice(tips)); tip_label.grid()

def reset():
    """Reset all test parameters for a new round"""
    global time_left, running, words_list, words
    time_left = INITIAL_TIME; running = False
    words_list, words = get_shuffled_words()  # Get new random words
    canvas.itemconfig(text_id, text="Press 'Start' to begin")
    label_time.config(text=f"Time: {time_left:02d}")
    clear_and_disable_entry()

def stop():
    """Stop the current test (with confirmation)"""
    global running, time_left
    if messagebox.askyesno("Stop test", "Are you ready to start again?"):
        running = False
        clear_and_disable_entry()
        tip_label.config(text=random.choice(tips)); tip_label.grid()
        label_time.config(text=f"Time: {time_left:02d}")
        window.title("Typing Speed Test: WELCOME!")
        reset()
    else:
        window.destroy()

def evaluate_text():
    """Calculate and display final results"""
    global running
    typed_words = entry.get("1.0","end-1c").split()
    score = calculate_score(typed_words, words_list)
    total_typed = len(typed_words)
    high = save_high_score_if_beaten(score)
    messagebox.showinfo(
        title="Result",
        message=f"Correct: {score} out of {total_typed}\nSpeed: {score} words per minute"
    )
    label_record.config(text=f"High Score = {high}")
    window.title("Typing Speed Test: WELCOME!")
    clear_and_disable_entry()
    reset()

# — Bind event handlers —
button_start.config(command=start)
button_pause.config(command=pause)
button_stop.config(command=stop)
entry.bind("<KeyRelease>", lambda e: color_text(entry, words_list))  # Realtime feedback