import random
import tkinter as tk
from tkinter import font as tkfont
 
class GuessGame:
    # Color palette
    BG        = "#0f0f1a"
    CARD      = "#1a1a2e"
    ACCENT    = "#e94560"
    ACCENT2   = "#0f3460"
    TEXT      = "#eaeaea"
    MUTED     = "#888aaa"
    SUCCESS   = "#2ecc71"
    WARNING   = "#f39c12"
    DANGER    = "#e74c3c"
 
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Number")
        self.root.geometry("480x560")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)
 
        self.secret       = random.randint(1, 100)
        self.attempts     = 0
        self.max_attempts = 10
        self.game_over    = False
 
        self._build_ui()
 
    # ── UI construction ──────────────────────────────────────────────────────
    def _build_ui(self):
        # ── header ──
        header = tk.Frame(self.root, bg=self.ACCENT2, pady=18)
        header.pack(fill="x")
 
        tk.Label(header, text="🎯  GUESS THE NUMBER",
                 font=("Courier New", 17, "bold"),
                 bg=self.ACCENT2, fg=self.ACCENT).pack()
        tk.Label(header, text="Find the secret number between 1 and 100",
                 font=("Courier New", 9),
                 bg=self.ACCENT2, fg=self.MUTED).pack(pady=(4, 0))
 
        # ── attempts bar ──
        bar_frame = tk.Frame(self.root, bg=self.BG, pady=18)
        bar_frame.pack(fill="x", padx=30)
 
        tk.Label(bar_frame, text="ATTEMPTS", font=("Courier New", 8, "bold"),
                 bg=self.BG, fg=self.MUTED).pack(anchor="w")
 
        self.bar_canvas = tk.Canvas(bar_frame, height=14, bg="#1e1e30",
                                    highlightthickness=0)
        self.bar_canvas.pack(fill="x", pady=(4, 0))
        self.bar_canvas.bind("<Configure>", self._draw_bar)
 
        self.attempts_label = tk.Label(bar_frame,
                                       text=f"0 / {self.max_attempts} attempts used",
                                       font=("Courier New", 9),
                                       bg=self.BG, fg=self.MUTED)
        self.attempts_label.pack(anchor="e", pady=(4, 0))
 
        # ── history box ──
        hist_frame = tk.Frame(self.root, bg=self.CARD, bd=0, pady=10, padx=14)
        hist_frame.pack(fill="both", expand=True, padx=30, pady=(0, 14))
 
        tk.Label(hist_frame, text="HISTORY", font=("Courier New", 8, "bold"),
                 bg=self.CARD, fg=self.MUTED).pack(anchor="w")
 
        self.history_text = tk.Text(hist_frame, height=8, width=40,
                                    bg=self.CARD, fg=self.TEXT,
                                    font=("Courier New", 10),
                                    bd=0, insertbackground=self.TEXT,
                                    state="disabled", wrap="word",
                                    selectbackground=self.ACCENT2)
        self.history_text.pack(fill="both", expand=True, pady=(6, 0))
 
        # tag colours
        self.history_text.tag_config("low",     foreground=self.WARNING)
        self.history_text.tag_config("high",    foreground=self.WARNING)
        self.history_text.tag_config("win",     foreground=self.SUCCESS)
        self.history_text.tag_config("lose",    foreground=self.DANGER)
        self.history_text.tag_config("muted",   foreground=self.MUTED)
 
        # ── input row ──
        input_frame = tk.Frame(self.root, bg=self.BG)
        input_frame.pack(padx=30, pady=(0, 10), fill="x")
 
        self.entry = tk.Entry(input_frame,
                              font=("Courier New", 18, "bold"),
                              justify="center", width=8,
                              bg="#1e1e30", fg=self.TEXT,
                              insertbackground=self.ACCENT,
                              relief="flat", bd=8,
                              highlightthickness=2,
                              highlightcolor=self.ACCENT,
                              highlightbackground="#2a2a4a")
        self.entry.pack(side="left", ipady=6)
        self.entry.bind("<Return>", lambda e: self._check_guess())
        self.entry.focus()
 
        self.submit_btn = tk.Button(input_frame, text="  GUESS  ",
                                    font=("Courier New", 12, "bold"),
                                    bg=self.ACCENT, fg="white",
                                    relief="flat", bd=0,
                                    activebackground="#c73652",
                                    activeforeground="white",
                                    cursor="hand2",
                                    command=self._check_guess)
        self.submit_btn.pack(side="left", padx=(10, 0), ipady=8, ipadx=4)
 
        # ── feedback label ──
        self.message_label = tk.Label(self.root, text="Make your first guess!",
                                      font=("Courier New", 11, "bold"),
                                      bg=self.BG, fg=self.MUTED)
        self.message_label.pack(pady=(0, 8))
 
        # ── play again ──
        self.replay_btn = tk.Button(self.root, text="↺  PLAY AGAIN",
                                    font=("Courier New", 10, "bold"),
                                    bg=self.ACCENT2, fg=self.TEXT,
                                    relief="flat", bd=0,
                                    activebackground="#163a6e",
                                    activeforeground="white",
                                    cursor="hand2",
                                    command=self._reset)
        self.replay_btn.pack(pady=(0, 18), ipadx=10, ipady=6)
 
    # ── progress bar ────────────────────────────────────────────────────────
    def _draw_bar(self, event=None):
        self.bar_canvas.delete("all")
        w = self.bar_canvas.winfo_width()
        h = 14
        ratio = self.attempts / self.max_attempts
        fill_w = int(w * ratio)
        color = self.SUCCESS if ratio < 0.6 else self.WARNING if ratio < 0.9 else self.DANGER
        self.bar_canvas.create_rectangle(0, 0, fill_w, h, fill=color, outline="")
 
    # ── game logic ──────────────────────────────────────────────────────────
    def _check_guess(self):
        if self.game_over:
            return
 
        raw = self.entry.get().strip()
        self.entry.delete(0, tk.END)
 
        try:
            guess = int(raw)
            if not (1 <= guess <= 100):
                raise ValueError
        except ValueError:
            self.message_label.config(text="⚠  Enter a number between 1 and 100",
                                       fg=self.DANGER)
            return
 
        self.attempts += 1
        self.attempts_label.config(
            text=f"{self.attempts} / {self.max_attempts} attempts used")
        self._draw_bar()
 
        if guess < self.secret:
            msg  = f"#{self.attempts:02d}  {guess}  →  Too LOW  ↑"
            tag  = "low"
            self.message_label.config(text="📉  Too low — try higher!", fg=self.WARNING)
        elif guess > self.secret:
            msg  = f"#{self.attempts:02d}  {guess}  →  Too HIGH  ↓"
            tag  = "high"
            self.message_label.config(text="📈  Too high — try lower!", fg=self.WARNING)
        else:
            msg  = f"#{self.attempts:02d}  {guess}  →  ✓ CORRECT!"
            tag  = "win"
            self.message_label.config(
                text=f"🎉  Found in {self.attempts} attempt(s)!", fg=self.SUCCESS)
            self.game_over = True
            self._append_history(msg, tag)
            return
 
        if self.attempts >= self.max_attempts:
            self.game_over = True
            self._append_history(msg, tag)
            self._append_history(f"   The number was {self.secret}.", "lose")
            self.message_label.config(
                text=f"💀  Game over! It was {self.secret}.", fg=self.DANGER)
            return
 
        self._append_history(msg, tag)
 
    def _append_history(self, text, tag="muted"):
        self.history_text.config(state="normal")
        self.history_text.insert("end", text + "\n", tag)
        self.history_text.see("end")
        self.history_text.config(state="disabled")
 
    def _reset(self):
        self.secret       = random.randint(1, 100)
        self.attempts     = 0
        self.game_over    = False
 
        self.attempts_label.config(text=f"0 / {self.max_attempts} attempts used")
        self.message_label.config(text="Make your first guess!", fg=self.MUTED)
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", "end")
        self.history_text.config(state="disabled")
        self._draw_bar()
        self.entry.focus()
 
 
root = tk.Tk()
app  = GuessGame(root)
root.mainloop()