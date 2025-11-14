import os
import re
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


COUNTDOWN_START = 5
MAX_ATTEMPTS = 5

MESSAGES = {
    5: "Hmm? Something’s off… Fill it again for Teto!",
    4: "Ehhh? Teto can’t find it… Try harder!",
    3: "Teto is staring right at you… Fill it properly this time~",
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
    root.iconbitmap(icon_path)
    root.title("Totally Not Malware")
    root.resizable(False, False)

    bg_main = "#FFE4EA"
    card_bg = "#EBEBEB"
    accent_blue = "#D84444"
    text_main = "#2E2E38"

    root.configure(bg=bg_main)

    width, height = 640, 320
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    card = tk.Frame(
        root,
        bg=card_bg,
        bd=0,
        highlightthickness=1,
        highlightbackground="#EBEBEB",
        highlightcolor="#EBEBEB"
    )
    card.pack(fill="both", expand=True, padx=16, pady=16)
    card.grid_columnconfigure(1, weight=1)

    img_frame = tk.Frame(
        card,
        width=220,
        height=220,
        bg="#EBEBEB",
        highlightthickness=1,
        highlightbackground="#EBEBEB",
        highlightcolor="#EBEBEB"
    )
    img_frame.grid(row=0, column=0, rowspan=3, padx=(12, 18), pady=12, sticky="n")
    img_frame.grid_propagate(False)

    img_path = os.path.join(base_dir, "teto.png")
    img = Image.open(img_path)
    img = img.resize((220, 220), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    img_label = tk.Label(img_frame, image=img_tk, bg="#EBEBEB")
    img_label.image = img_tk
    img_label.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(
        card,
        text="Heeey~",
        bg=card_bg,
        fg=accent_blue,
        font=("Segoe UI", 16, "bold")
    )
    title_label.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=(16, 4))

    msg_label = tk.Label(
        card,
        text="Do you th-think I could have your credit card information! P-please?",
        bg=card_bg,
        fg=text_main,
        font=("Segoe UI", 10),
        justify="left",
        wraplength=380
    )
    msg_label.grid(row=1, column=1, sticky="w", padx=(0, 12), pady=(0, 8))

    form_frame = tk.Frame(card, bg=card_bg)
    form_frame.grid(row=2, column=1, sticky="nsew", padx=(0, 12), pady=(0, 12))

    label_font = ("Segoe UI", 10)
    entry_width = 30

    tk.Label(
        form_frame,
        text="Card number:",
        bg=card_bg,
        fg=text_main,
        font=label_font
    ).grid(row=0, column=0, sticky="e", pady=3, padx=(0, 6))

    tk.Label(
        form_frame,
        text="Expiry date:",
        bg=card_bg,
        fg=text_main,
        font=label_font
    ).grid(row=1, column=0, sticky="e", pady=3, padx=(0, 6))

    tk.Label(
        form_frame,
        text="Security code:",
        bg=card_bg,
        fg=text_main,
        font=label_font
    ).grid(row=2, column=0, sticky="e", pady=3, padx=(0, 6))

    e1 = tk.Entry(
        form_frame,
        width=entry_width,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#EBEBEB",
        highlightcolor="#EBEBEB"
    )
    e2 = tk.Entry(
        form_frame,
        width=entry_width,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#EBEBEB",
        highlightcolor="#EBEBEB"
    )
    e3 = tk.Entry(
        form_frame,
        width=entry_width,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#EBEBEB",
        highlightcolor="#EBEBEB"
    )

    e1.grid(row=0, column=1, sticky="w", pady=3)
    e2.grid(row=1, column=1, sticky="w", pady=3)
    e3.grid(row=2, column=1, sticky="w", pady=3)

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
        value = e2.get()
        cursor = e2.index(tk.INSERT)
        if cursor != len(value):
            return
        digits = "".join(ch for ch in value if ch.isdigit())[:4]
        n = len(digits)
        if n == 0:
            formatted = ""
        elif n == 1:
            d = digits
            if d == "0":
                formatted = ""
            else:
                formatted = f"0{d}"
        elif n == 2:
            m = int(digits)
            if m <= 0:
                m = 1
            elif m > 12:
                m = 12
            formatted = f"{m:02d}"
        elif n == 3:
            m = int(digits[:2])
            if m <= 0:
                m = 1
            elif m > 12:
                m = 12
            y = digits[2]
            formatted = f"{m:02d}/{y}"
        else:
            m = int(digits[:2])
            if m <= 0:
                m = 1
            elif m > 12:
                m = 12
            yy = digits[2:]
            formatted = f"{m:02d}/{yy}"
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
        value = e2.get()
        cursor = e2.index(tk.INSERT)
        digits = "".join(ch for ch in value if ch.isdigit())
        if cursor == len(value) and len(digits) >= 4:
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

    bottom = tk.Frame(root, bg=bg_main)
    bottom.pack(fill="x", side="bottom", padx=16, pady=(0, 12))

    countdown_label = tk.Label(
        bottom,
        text="",
        bg=bg_main,
        fg="#EBEBEB",
        font=("Consolas", 10),
        justify="center"
    )

    btn_frame = tk.Frame(bottom, bg=bg_main)
    btn_frame.pack(pady=(0, 6))

    def style_button(btn: tk.Button):
        btn.configure(
            bg="#f3f6ff",
            fg=text_main,
            activebackground="#EBEBEB",
            activeforeground=text_main,
            relief="flat",
            bd=1,
            highlightthickness=1,
            highlightbackground="#EBEBEB",
            highlightcolor="#EBEBEB",
            font=("Segoe UI", 10),
            width=10
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
                fg="#1A0400"
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
        btn_frame.pack_forget()
        countdown_label.config(
            text="Teto is preparing a cute BONK in 5...",
            fg="#e23b3b",
            font=("Consolas", 10),
            justify="center"
        )
        countdown_label.pack(pady=8)
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
            "Hey! That was the second time! Teto is getting suspicious…",
            "Hmm… Why do you keep pressing that? Teto doesn’t approve.",
            "Fourth time?! Teto will block the door at this rate!",
            "Again?! You’re making Teto puff her cheeks!",
            "Stop that! Teto is not letting you escape!!",
            "Please… Just cooperate with Teto…",
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

    yes_btn = tk.Button(btn_frame, text="Th-thanks", width=10, command=on_yes)
    no_btn = tk.Button(btn_frame, text="No", width=10, command=on_no)

    style_button(yes_btn)
    style_button(no_btn)

    yes_btn.pack(side="left", padx=4)
    no_btn.pack(side="left", padx=4)

    root.mainloop()


if __name__ == "__main__":
    main()
