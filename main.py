#Writer Batuhan Ozbay
import math
import time
import pygame
from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
WHITE_BLUE = "#36C2CE"
SEA_GREEN = "#77E4C8"
DARK_GREEN = "#808836"
NAVY_BLUE = "#17153B"
BROWN = "#948979"
SKIN_COLOR = "#F7E7DC"
FONT_NAME = "Courier"

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps = 0
timer = None
is_paused = False
paused_time = 0
is_running = False

pygame.mixer.init()

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global reps, is_paused, paused_time, is_running
    if timer:
        window.after_cancel(timer)
    music_staves_canvas.itemconfig(timer_text, text="00:00")
    label_title.config(text="Timer")
    check_marks_lbl.config(text="")
    reps = 0
    is_paused = False
    paused_time = 0
    is_running = False
    pygame.mixer.music.stop()

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global reps, is_paused, is_running
    if not is_running or is_paused:
        is_paused = False
        is_running = True
        if paused_time > 0:
            count_down(paused_time)
        else:
            reps += 1
            work_sec = WORK_MIN * 60
            short_break_sec = SHORT_BREAK_MIN * 60
            long_break_sec = LONG_BREAK_MIN * 60
            if reps % 8 == 0:
                count_down(long_break_sec)
                label_title.config(text="Break", fg=RED)
                check_marks_lbl.config(text=reps * "✔", font=(FONT_NAME, 24, "bold"))
            elif reps % 2 == 0:
                count_down(short_break_sec)
                label_title.config(text="Break", fg=PINK)
            else:
                count_down(work_sec)
                label_title.config(text="Work", fg=BROWN)

# ---------------------------- PAUSE TIMER ------------------------------- #


def pause_timer():
    global timer, is_paused, paused_time
    if timer and not is_paused:
        is_paused = True
        window.after_cancel(timer)
        current_time = music_staves_canvas.itemcget(timer_text, 'text')
        minutes, seconds = map(int, current_time.split(':'))
        paused_time = minutes * 60 + seconds

# ---------------------------- PLAY MUSIC ------------------------------- #


def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    global is_running, paused_time
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    music_staves_canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        is_running = False
        paused_time = 0
        if reps % 2 == 1:
            play_music("PinkPanther.mp3")
        start_timer()
        mark = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            mark += "✔"
            check_marks_lbl.config(text=mark, font=(FONT_NAME, 24, "bold"), padx=5, pady=5)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Blue Period Pomodoro")
window.config(padx=30, pady=30, bg=SKIN_COLOR)


def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time, fg=NAVY_BLUE)
    window.after(1000, update_clock)


clock_label = Label(window, font=(FONT_NAME, 20, "bold"), bg=SKIN_COLOR, fg=DARK_GREEN)
clock_label.grid(column=1, row=0, padx=10, pady=10)
update_clock()

yatora = PhotoImage(file="file_resized.png")
yatora_canvas = Canvas(width=350, height=300, bg=SKIN_COLOR, highlightthickness=0)
yatora_canvas.create_image(175, 150, image=yatora)
yatora_canvas.grid(column=1, row=2)

music_staves = PhotoImage(file="music_resized.png")
music_staves_canvas = Canvas(width=200, height=200, bg=SKIN_COLOR, highlightthickness=0)
music_staves_canvas.create_image(100, 100, image=music_staves)
timer_text = music_staves_canvas.create_text(100, 100, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
music_staves_canvas.grid(column=1, row=3)


label_title = Label(text="Timer", font=(FONT_NAME, 50, "bold"), bg=SKIN_COLOR, fg=DARK_GREEN)
label_title.config(text="Timer")
label_title.grid(column=1, row=1, padx=10, pady=10)


def initial_countdown(count):
    if count >= 0:
        music_staves_canvas.itemconfig(timer_text, text=f"{count}")
        window.after(1000, initial_countdown, count - 1)
    else:
        start_timer()


initial_countdown(5)

# Check marks label setup
check_marks_lbl = Label(text="", fg=GREEN, bg=SKIN_COLOR, font=(FONT_NAME, 15, "bold"))
check_marks_lbl.grid(column=1, row=5)

# Buttons setup
btn_start = Button(text="Start", command=start_timer)
btn_start.grid(column=0, row=4)

btn_reset = Button(text="Reset", command=reset_timer)
btn_reset.grid(column=2, row=4)

btn_pause = Button(text="Pause", command=pause_timer)
btn_pause.grid(column=1, row=4)


window.mainloop()
