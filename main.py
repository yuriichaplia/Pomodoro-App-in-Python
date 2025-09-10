import math
import tkinter

# ---------------------------- CONSTANTS ------------------------------- #
REPS = 0
timer = ""
WORK_MIN = 25
RED = "#e7305b"
PINK = "#e2979c"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
LONG_BREAK_MIN = 20
SHORT_BREAK_MIN = 5
FONT_NAME = "Courier"
START_BUTTON_PRESSED = False

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    try:
        window.after_cancel(timer)
    except ValueError:
        pass

    canvas.itemconfig(text_countdown, text="00:00")
    timer_label.config(text="Timer", fg=GREEN, font=(FONT_NAME, 35, "bold"), bg=YELLOW)
    checkmark.config(text="")
    global REPS, START_BUTTON_PRESSED
    REPS = 0
    START_BUTTON_PRESSED = False

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global REPS
    REPS += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if REPS == 8:
        count_start(long_break_sec)
        timer_label.config(text="Break", fg=RED, font=(FONT_NAME, 35, "bold"), bg=YELLOW)
    elif REPS % 2 != 0:
        count_start(work_sec)
        timer_label.config(text="Work", fg=GREEN, font=(FONT_NAME, 35, "bold"), bg=YELLOW)
    elif REPS % 2 == 0:
        count_start(short_break_sec)
        timer_label.config(text="Break", fg=PINK, font=(FONT_NAME, 35, "bold"), bg=YELLOW)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_start(count):
    global REPS, timer
    count_min = math.floor(count/60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(text_countdown, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_start, count-1)
    else:
        if REPS % 2 != 0:
            textmark = ""
            for _ in range(int((REPS+1)/2)):
                textmark += "✔"
            checkmark.config(text=textmark)

        if REPS == 8:
            REPS = 0

        start_timer()

# ---------------------------- BLOCKING START BUTTON ------------------------------- #
def combine_functions(function):
    def combined_functions(*args, **kwargs):
        global START_BUTTON_PRESSED
        if not START_BUTTON_PRESSED:
            function(*args, **kwargs)
        START_BUTTON_PRESSED = True
    return combined_functions

# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Pomodoro App")
window.minsize(width=400, height=300)
window.config(padx=100, pady=20, bg=YELLOW)

timer_label = tkinter.Label(text="Timer", fg=GREEN, font=(FONT_NAME, 35, "bold"), bg=YELLOW)
timer_label.grid(column=1, row=0)

canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = tkinter.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_image)
text_countdown = canvas.create_text(100, 130, text="00:00", fill = "white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = tkinter.Button(text="Start", highlightthickness=0, command=combine_functions(start_timer))
start_button.grid(column=0, row=2)

reset_button = tkinter.Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

checkmark = tkinter.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 10, "bold"))
checkmark.grid(column=1, row=3)

window.mainloop()