import os
import re
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


COUNTDOWN_START = 5
MAX_ATTEMPTS = 5

MESSAGES = {
    5: "Hmm? Something's off... Fill it again for Teto!",
    4: "Ehhh? Teto can't find it... Try harder!",
    3: "Teto is staring right at you... Fill it properly this time~",
    2: "Are you messing with Teto on purpose? Fix it!",
    1: "Last chance! Fill it correctly before Teto gets mad!",
    0: "Your information was not found! Teto will hack your Facebook account for not being honest!"
}


def main():
    attempts_left = MAX_ATTEMPTS
    close_attempts = 0

    root = tk.Tk()
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    icon_path = os.path.join(base_dir, "teto.ico")
    try:
        root.iconbitmap(icon_path)
    except Exception:
        pass
    root.title("Totally not Malware")
    root.resizable(False, False)

    bg_root = "#0d0b1a"
    bg_panel = "#141129"
    card_bg = "#1b1736"
    line = "#2a2745"
    accent = "#ff6b6b"
    accent_soft = "#ffd166"
    text_main = "#f8f9ff"
    text_subtle = "#c7c9d9"
    blur = "#090812"

    width, height = 780, 420
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg=bg_root)

    gradient = tk.Canvas(root, highlightthickness=0, bd=0, bg=bg_root, width=width, height=height)
    gradient.place(relx=0, rely=0, relwidth=1, relheight=1)
    for i, color in enumerate(("#191734", "#13142c", "#0d0b1a")):
        gradient.create_rectangle(
            0, i * (height // 3), width, (i + 1) * (height // 3), fill=color, outline=""
        )

    outer = tk.Frame(root, bg=bg_root, padx=18, pady=18)
    outer.pack(fill="both", expand=True)

    shell = tk.Frame(outer, bg=blur)
    shell.pack(fill="both", expand=True)

    card = tk.Frame(shell, bg=card_bg, bd=0, highlightthickness=1, highlightbackground=line, highlightcolor=line)
    card.pack(fill="both", expand=True, padx=6, pady=6)
    card.grid_columnconfigure(1, weight=1)

    img_frame = tk.Frame(card, bg=card_bg, width=250, height=260)
    img_frame.grid(row=0, column=0, rowspan=4, padx=(16, 22), pady=16, sticky="n")
    img_frame.grid_propagate(False)

    halo = tk.Frame(img_frame, bg=line, width=240, height=240)
    halo.place(relx=0.5, rely=0.5, anchor="center")

    portrait = tk.Frame(halo, bg=bg_panel, width=230, height=230, highlightthickness=1, highlightbackground=line)
    portrait.place(relx=0.5, rely=0.5, anchor="center")
    portrait.grid_propagate(False)

    img_path = os.path.join(base_dir, "teto.png")
    try:
        img = Image.open(img_path)
        img = img.resize((220, 220), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        img_label = tk.Label(portrait, image=img_tk, bg=bg_panel)
        img_label.image = img_tk
        img_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        img_label = tk.Label(portrait, text="(image missing)", fg=text_subtle, bg=bg_panel)
        img_label.place(relx=0.5, rely=0.5, anchor="center")

    header = tk.Frame(card, bg=card_bg)
    header.grid(row=0, column=1, sticky="ew", padx=(0, 14), pady=(18, 0))

    badge = tk.Label(
        header,
        text="Teto Request",
        bg=card_bg,
        fg=accent,
        font=("Segoe UI", 9, "bold"),
        padx=12,
        pady=4
    )
    badge.pack(side="left")

    title_label = tk.Label(
        card,
        text="Heeey, share your secrets?",
        bg=card_bg,
        fg=text_main,
        font=("Segoe UI Semibold", 20)
    )
    title_label.grid(row=1, column=1, sticky="w", padx=(0, 14))

    msg_label = tk.Label(
        card,
        text="Do you th-think I could have your credit card information? P-please!",
        bg=card_bg,
        fg=text_subtle,
        font=("Segoe UI", 11),
        wraplength=430,
        justify="left"
    )
    msg_label.grid(row=2, column=1, sticky="w", padx=(0, 14), pady=(4, 2))

    form_frame = tk.Frame(card, bg=card_bg)
    form_frame.grid(row=3, column=1, sticky="nsew", padx=(0, 14), pady=(10, 0))
    form_frame.grid_columnconfigure(1, weight=1)

    tk.Frame(form_frame, bg=line, height=1).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

    label_font = ("Segoe UI", 10)
    entry_kwargs = {
        "width": 28,
        "relief": "flat",
        "bg": bg_panel,
        "fg": text_main,
        "insertbackground": accent,
        "highlightthickness": 1,
        "highlightbackground": line,
        "highlightcolor": accent,
        "disabledbackground": bg_panel,
        "disabledforeground": text_subtle
    }

    tk.Label(
        form_frame,
        text="Card number",
        bg=card_bg,
        fg=text_subtle,
        font=label_font
    ).grid(row=2, column=0, sticky="e", pady=5, padx=(0, 10))

    tk.Label(
        form_frame,
        text="Expiry date (MM/YY)",
        bg=card_bg,
        fg=text_subtle,
        font=label_font
    ).grid(row=3, column=0, sticky="e", pady=5, padx=(0, 10))

    tk.Label(
        form_frame,
        text="Security code",
        bg=card_bg,
        fg=text_subtle,
        font=label_font
    ).grid(row=4, column=0, sticky="e", pady=5, padx=(0, 10))

    e1 = tk.Entry(form_frame, **entry_kwargs)
    e2 = tk.Entry(form_frame, **entry_kwargs)
    e3 = tk.Entry(form_frame, **entry_kwargs, show="*")

    e1.grid(row=2, column=1, sticky="w", pady=5)
    e2.grid(row=3, column=1, sticky="w", pady=5)
    e3.grid(row=4, column=1, sticky="w", pady=5)

    action_frame = tk.Frame(card, bg=card_bg)
    action_frame.grid(row=4, column=1, sticky="ew", padx=(0, 14), pady=(14, 12))
    action_frame.grid_columnconfigure(0, weight=1)

    countdown_label = tk.Label(
        action_frame,
        text="",
        bg=card_bg,
        fg=text_subtle,
        font=("Consolas", 10),
        justify="left"
    )
    countdown_label.grid(row=0, column=0, sticky="w")

    btn_frame = tk.Frame(action_frame, bg=card_bg)
    btn_frame.grid(row=0, column=1, sticky="e", padx=(8, 0))

    def style_button(btn: tk.Button, primary: bool = False):
        base_bg = accent if primary else "#26243d"
        base_fg = text_main if primary else text_subtle
        btn.configure(
            bg=base_bg,
            fg=base_fg,
            activebackground=accent if primary else "#2f2b4d",
            activeforeground=text_main,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=line,
            highlightcolor=accent,
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=8,
            cursor="hand2"
        )

    def has_all_input():
        return all(field.get().strip() for field in (e1, e2, e3))

    def validate_payment_inputs() -> bool:
        card_number_raw = e1.get().strip()
        expiry = e2.get().strip()
        cvv = e3.get().strip()
        digits = "".join(ch for ch in card_number_raw if ch.isdigit())
        if not (len(digits) == 16 and digits.startswith("4")):
            messagebox.showwarning(
                "Invalid Card Number",
                "A Visa card must be 16 digits and start with 4."
            )
            return False
        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", expiry):
            messagebox.showwarning(
                "Invalid Expiry Date",
                "Expiry date must be in MM/YY format (e.g. 07/28)."
            )
            return False
        if not re.fullmatch(r"\d{3}", cvv):
            messagebox.showwarning(
                "Invalid CVV",
                "Security code (CVV) must be exactly 3 digits."
            )
            return False
        return True

    def format_card_number(event=None):
        if event and event.keysym in ("Left", "Right", "Home", "End", "Tab", "Shift_L", "Shift_R"):
            return
        value = e1.get()
        cursor = e1.index(tk.INSERT)
        if cursor != len(value):
            return
        digits = "".join(ch for ch in value if ch.isdigit())[:16]
        groups = [digits[i:i + 4] for i in range(0, len(digits), 4)]
        formatted = "-".join(groups)
        e1.delete(0, tk.END)
        e1.insert(0, formatted)
        e1.icursor(len(formatted))

    def format_expiry(event=None):
        if event and event.keysym in ("Left", "Right", "Home", "End", "Tab", "Shift_L", "Shift_R"):
            return
        digits = "".join(ch for ch in e2.get() if ch.isdigit())[:4]
        if not digits:
            formatted = ""
        else:
            first = int(digits[0])
            if len(digits) == 1:
                formatted = f"0{first}/" if first > 2 else digits
            elif len(digits) == 2:
                if first > 2:
                    month = f"0{first}"
                    year_part = digits[1]
                    formatted = f"{month}/{year_part}"
                else:
                    m = int(digits[:2])
                    m = max(1, min(m, 12))
                    formatted = f"{m:02d}"
            else:
                if first > 2:
                    month = f"0{first}"
                    rest = digits[1:]
                    formatted = f"{month}/{rest}"
                else:
                    month_raw = int(digits[:2])
                    month_raw = max(1, min(month_raw, 12))
                    month = f"{month_raw:02d}"
                    rest = digits[2:]
                    formatted = month if not rest else f"{month}/{rest}"
        e2.delete(0, tk.END)
        e2.insert(0, formatted)
        e2.icursor(len(formatted))

    def format_cvv(event=None):
        if event and event.keysym in ("Left", "Right", "Home", "End", "Tab", "Shift_L", "Shift_R"):
            return
        value = e3.get()
        cursor = e3.index(tk.INSERT)
        if cursor != len(value):
            return
        digits = "".join(ch for ch in value if ch.isdigit())[:3]
        e3.delete(0, tk.END)
        e3.insert(0, digits)
        e3.icursor(len(digits))

    def limit_card_digits(event):
        if not event.char.isdigit():
            return
        value = e1.get()
        cursor = e1.index(tk.INSERT)
        digits = "".join(ch for ch in value if ch.isdigit())
        if cursor == len(value) and len(digits) >= 16:
            return "break"

    def limit_expiry_digits(event):
        if not event.char.isdigit():
            return
        digits = "".join(ch for ch in e2.get() if ch.isdigit())
        if len(digits) >= 4:
            return "break"

    def limit_cvv_digits(event):
        if not event.char.isdigit():
            return
        value = e3.get()
        cursor = e3.index(tk.INSERT)
        digits = "".join(ch for ch in value if ch.isdigit())
        if cursor == len(value) and len(digits) >= 3:
            return "break"

    e1.bind("<KeyPress>", limit_card_digits)
    e1.bind("<KeyRelease>", format_card_number)

    e2.bind("<KeyPress>", limit_expiry_digits)
    e2.bind("<KeyRelease>", format_expiry)

    e3.bind("<KeyPress>", limit_cvv_digits)
    e3.bind("<KeyRelease>", format_cvv)

    def start_countdown():
        for b in (yes_btn, no_btn):
            b.config(state="disabled")

        def tick(i):
            if i < 0:
                countdown_label.config(text="")
                messagebox.showinfo(
                    "Teto's Response",
                    MESSAGES[attempts_left]
                )
                root.destroy()
                return
            countdown_label.config(
                text=f"Teto is preparing a cute BONK in {i}...",
                fg=accent_soft
            )
            root.after(1000, tick, i - 1)

        tick(COUNTDOWN_START)

    def on_yes():
        nonlocal attempts_left
        if not has_all_input():
            messagebox.showwarning(
                "Teto is confused!",
                "Teto needs ALL the fields filled! Please fill them all!"
            )
            return
        if not validate_payment_inputs():
            return
        if attempts_left > 0:
            messagebox.showinfo(
                "Teto's Response",
                MESSAGES[attempts_left]
            )
            attempts_left -= 1
            if attempts_left > -1:
                return
        yes_btn.pack_forget()
        no_btn.pack_forget()
        btn_frame.grid_forget()
        countdown_label.config(
            text="Teto is preparing a cute BONK in 5...",
            fg=accent,
            font=("Consolas", 10),
            justify="left"
        )
        start_countdown()

    def on_no():
        messagebox.showinfo(
            "Teto is sulking...",
            "Please refill the information...\nOr I will hack your Facebook account!"
        )

    def on_close():
        nonlocal close_attempts
        close_attempts += 1
        messages_seq = [
            "Teto noticed you~\nTrying to escape from Teto?\nPlease go back and fill the information!",
            "Hey! That was the second time! Teto is getting suspicious...",
            "Hmm... Why do you keep pressing that? Teto doesn't approve.",
            "Fourth time?! Teto will block the door at this rate!",
            "Again?! You're making Teto puff her cheeks!",
            "Stop that! Teto is not letting you escape!!",
            "Please... Just cooperate with Teto...",
            "Eighth time?? Are you doing this on purpose?!",
            "Last warning! One more attempt and Teto snaps!!"
        ]
        if close_attempts <= 9:
            messagebox.showinfo("Teto noticed you~", messages_seq[close_attempts - 1])
            return
        messagebox.showinfo(
            "Teto noticed you~",
            "Fine!! You really want to leave, huh?! Teto will let you go..."
        )
        messagebox.showinfo(
            "Teto's Final Message",
            "Your computer has been hacked!"
        )
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    yes_btn = tk.Button(btn_frame, text="Submit to Teto", command=on_yes)
    no_btn = tk.Button(btn_frame, text="No thanks", command=on_no)

    style_button(yes_btn, primary=True)
    style_button(no_btn)

    yes_btn.pack(side="left", padx=6)
    no_btn.pack(side="left", padx=6)

    root.mainloop()


if __name__ == "__main__":
    main()
