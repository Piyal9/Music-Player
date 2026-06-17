import os
import tkinter as tk
from tkinter import filedialog, ttk
import pygame

# Initialize pygame mixer safely
try:
    pygame.mixer.init()
except Exception:
    # mixer might already be initialized or no audio device available
    pass

# State
filename = None

# Utilities
def _short_name(path, length=30):
    if not path:
        return "No file loaded"
    name = os.path.basename(path)
    if len(name) > length:
        return name[: length - 3] + "..."
    return name

def _ms_to_mmss(ms):
    if ms < 0:
        return "00:00"
    s = int(ms // 1000)
    m = s // 60
    s = s % 60
    return f"{m:02d}:{s:02d}"

# Actions
def load_song():
    global filename
    path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")),
    )
    if path:
        filename = path
        song_label.config(text=_short_name(filename))

def play_song():
    if not filename:
        status_label.config(text="No file. Click Load.")
        return
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(volume_var.get() / 100)
        progress_bar.start(50)
        status_label.config(text="Playing")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def pause_song():
    try:
        pygame.mixer.music.pause()
        progress_bar.stop()
        status_label.config(text="Paused")
    except Exception:
        pass

def resume_song():
    try:
        pygame.mixer.music.unpause()
        progress_bar.start(50)
        status_label.config(text="Playing")
    except Exception:
        pass

def stop_song():
    try:
        pygame.mixer.music.stop()
        progress_bar.stop()
        elapsed_label.config(text="00:00")
        status_label.config(text="Stopped")
    except Exception:
        pass

def set_volume(v):
    try:
        pygame.mixer.music.set_volume(float(v) / 100)
    except Exception:
        pass

def update_elapsed():
    try:
        pos = pygame.mixer.music.get_pos()
        if pos == -1:
            # Not playing
            pass
        else:
            elapsed_label.config(text=_ms_to_mmss(pos))
    except Exception:
        pass
    root.after(500, update_elapsed)

def _make_button(master, text, cmd, bg="#0ea5a4", fg="#ffffff"):
    b = tk.Button(master, text=text, command=cmd, bg=bg, fg=fg, bd=0, relief="flat",
                  activebackground="#14b8a6", activeforeground="#ffffff", padx=12, pady=8)
    b.bind("<Enter>", lambda e: b.config(bg="#14b8a6"))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b

# GUI Window
root = tk.Tk()
root.title("Piyal — Music")
root.geometry("520x260")
root.resizable(False, False)

# Colors and fonts
BG = "#0f172a"
CARD = "#0b1220"
FG = "#e6edf3"
ACCENT = "#06b6d4"
root.configure(bg=BG)
default_font = ("Segoe UI", 10)

# Top frame (title)
top = tk.Frame(root, bg=BG)
top.pack(fill="x", padx=12, pady=(12, 6))
title = tk.Label(top, text="Music Player", bg=BG, fg=FG, font=("Segoe UI", 14, "bold"))
title.pack(side="left")

# Card
card = tk.Frame(root, bg=CARD, bd=0, relief="flat")
card.pack(fill="both", expand=False, padx=12, pady=6)

song_label = tk.Label(card, text="No file loaded", font=("Segoe UI", 11), bg=CARD, fg=FG)
song_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(12, 6))

elapsed_label = tk.Label(card, text="00:00", font=("Segoe UI", 9), bg=CARD, fg="#9ca3af")
elapsed_label.grid(row=1, column=0, sticky="w", padx=12)

status_label = tk.Label(card, text="Idle", font=("Segoe UI", 9), bg=CARD, fg="#9ca3af")
status_label.grid(row=1, column=1, sticky="w")

progress_bar = ttk.Progressbar(card, mode="indeterminate", length=260)
progress_bar.grid(row=2, column=0, columnspan=3, padx=12, pady=(8, 12))

# Controls frame
controls = tk.Frame(card, bg=CARD)
controls.grid(row=3, column=0, columnspan=3, pady=(0, 12))

btn_load = _make_button(controls, "📂 Load", load_song, bg=ACCENT)
btn_load.grid(row=0, column=0, padx=6)

btn_play = _make_button(controls, "▶ Play", play_song, bg="#10b981")
btn_play.grid(row=0, column=1, padx=6)

btn_pause = _make_button(controls, "⏸ Pause", pause_song, bg="#f59e0b")
btn_pause.grid(row=0, column=2, padx=6)

btn_resume = _make_button(controls, "⏯ Resume", resume_song, bg="#3b82f6")
btn_resume.grid(row=0, column=3, padx=6)

btn_stop = _make_button(controls, "⏹ Stop", stop_song, bg="#ef4444")
btn_stop.grid(row=0, column=4, padx=6)

# Volume
volume_var = tk.DoubleVar(value=80)
vol_frame = tk.Frame(card, bg=CARD)
vol_frame.grid(row=0, column=3, rowspan=4, padx=(12, 18), pady=12)
vol_label = tk.Label(vol_frame, text="Volume", bg=CARD, fg=FG, font=("Segoe UI", 10))
vol_label.pack(anchor="e")
vol_slider = ttk.Scale(vol_frame, from_=0, to=100, orient="vertical", variable=volume_var, command=set_volume)
vol_slider.pack(ipadx=6, ipady=6, pady=6)

# Kick off elapsed updater
root.after(500, update_elapsed)

root.mainloop()
