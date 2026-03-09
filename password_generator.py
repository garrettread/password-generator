import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox
from storage import save_password_record
from password_checker_connector import score_password

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = string.punctuation

HEX_CHARS = "0123456789ABCDEF"
SIMILAR_CHARS = set("iIlL1oO0")

MAX_RAW_SCORE = 115


class PasswordGeneratorPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=24)
        self.controller = controller
        self.advanced_visible = True

        self.lowercaseCheck = tk.IntVar(value=1)
        self.uppercaseCheck = tk.IntVar(value=1)
        self.digitCheck = tk.IntVar(value=1)
        self.symbolCheck = tk.IntVar(value=1)

        self.excludeSimilarCheck = tk.IntVar(value=0)
        self.hexadecimalCheck = tk.IntVar(value=0)

        self.numberSelect = tk.IntVar(value=16)
        self.password_displayed = tk.StringVar(value="Generating...")
        self.suggestions_text = tk.StringVar(value="Strong password suggestions will appear here!")
        self.score_text = tk.StringVar(value="Score: 0 / 115")

        self._setup_progress_styles()
        self._build_ui()
        self.after(1, self.passwordGen)

    def _setup_progress_styles(self):
        style = ttk.Style(self)

        style.configure(
            "Weak.Horizontal.TProgressbar",
            troughcolor="#e6e6e6",
            background="#c0392b",
            bordercolor="#e6e6e6",
            lightcolor="#c0392b",
            darkcolor="#c0392b",
        )
        style.configure(
            "Medium.Horizontal.TProgressbar",
            troughcolor="#e6e6e6",
            background="#e67e22",
            bordercolor="#e6e6e6",
            lightcolor="#e67e22",
            darkcolor="#e67e22",
        )
        style.configure(
            "Good.Horizontal.TProgressbar",
            troughcolor="#e6e6e6",
            background="#8dbb45",
            bordercolor="#e6e6e6",
            lightcolor="#8dbb45",
            darkcolor="#8dbb45",
        )
        style.configure(
            "Strong.Horizontal.TProgressbar",
            troughcolor="#e6e6e6",
            background="#5fb654",
            bordercolor="#e6e6e6",
            lightcolor="#5fb654",
            darkcolor="#5fb654",
        )

    def _build_ui(self):
        outer = ttk.Frame(self)
        outer.pack(fill="both", expand=True)

        topbar = ttk.Frame(outer)
        topbar.pack(fill="x", pady=(0, 10))

        back_button = ttk.Button(
            topbar,
            text="← Back",
            command=lambda: self.controller.show_frame("HomePage")
        )
        back_button.pack(side="left")

        title_label = ttk.Label(
            outer,
            text="Password Generator",
            style="Hero.TLabel"
        )
        title_label.pack(pady=(2, 6))

        subtitle_label = ttk.Label(
            outer,
            text="Designed to Emulate RoboForm's Password Generator.",
            style="Body.TLabel",
            wraplength=760,
            justify="center"
        )
        subtitle_label.pack(pady=(0, 18))

        self.strength_label = tk.Label(
            outer,
            text="",
            font=("Helvetica", 16, "bold"),
            bg=self.controller.cget("bg"),
            fg="#222222"
        )
        self.strength_label.pack(pady=(2, 14))

        generator_card = ttk.Frame(outer, style="Card.TFrame", padding=22)
        generator_card.pack(fill="x", padx=28)

        main_row = ttk.Frame(generator_card, style="Card.TFrame")
        main_row.pack(fill="x", pady=(0, 14))

        spin_number = ttk.Spinbox(
            main_row,
            from_=1,
            to=512,
            textvariable=self.numberSelect,
            width=5
        )
        spin_number.pack(side="left", padx=(0, 12), ipady=6)

        self.password_label = tk.Label(
            main_row,
            textvariable=self.password_displayed,
            fg="white",
            bg="#2f6f3e",
            font=("Consolas", 16, "bold"),
            anchor="w",
            padx=16,
            pady=14
        )
        self.password_label.pack(side="left", fill="x", expand=True, padx=(0, 12))

        self.calculate_button = tk.Button(
            main_row,
            text="Generate",
            command=self.passwordGen,
            relief="flat",
            borderwidth=0,
            activeforeground="white",
            bg="#2f6f3e",
            fg="white",
            activebackground="#2f6f3e",
            font=("Helvetica", 10, "bold"),
            padx=16,
            pady=8
        )
        self.calculate_button.pack(side="left", padx=(0, 10))

        clip_button = ttk.Button(
            main_row,
            text="Copy",
            style="Primary.TButton",
            command=self.clipboardFun
        )
        clip_button.pack(side="left", padx=(0, 10), ipady=4)

        save_button = ttk.Button(
            main_row,
            text="Save",
            style="Primary.TButton",
            command=self.open_save_popup
        )
        save_button.pack(side="left", ipady=4)

        options_card = ttk.Frame(generator_card, style="Card.TFrame")
        options_card.pack(fill="x")

        top_options_row = ttk.Frame(options_card, style="Card.TFrame")
        top_options_row.pack(fill="x", pady=(0, 10))

        options_title = ttk.Label(
            top_options_row,
            text="Included Character Sets",
            style="SectionTitle.TLabel"
        )
        options_title.pack(side="left")

        self.advanced_toggle_button = ttk.Button(
            top_options_row,
            text="Advanced Settings ▲",
            command=self.toggle_advanced_settings
        )
        self.advanced_toggle_button.pack(side="right")

        checks_row = ttk.Frame(options_card, style="Card.TFrame")
        checks_row.pack(anchor="w", pady=(0, 8))

        upper_checkbox = ttk.Checkbutton(
            checks_row, text="A - Z", variable=self.uppercaseCheck, onvalue=1, offvalue=0
        )
        upper_checkbox.pack(side="left", padx=(0, 18))

        lower_checkbox = ttk.Checkbutton(
            checks_row, text="a - z", variable=self.lowercaseCheck, onvalue=1, offvalue=0
        )
        lower_checkbox.pack(side="left", padx=(0, 18))

        digit_checkbox = ttk.Checkbutton(
            checks_row, text="0 - 9", variable=self.digitCheck, onvalue=1, offvalue=0
        )
        digit_checkbox.pack(side="left", padx=(0, 18))

        symbol_checkbox = ttk.Checkbutton(
            checks_row, text="Symbols", variable=self.symbolCheck, onvalue=1, offvalue=0
        )
        symbol_checkbox.pack(side="left", padx=(0, 18))

        self.advanced_frame = ttk.Frame(options_card, style="Card.TFrame")
        self.advanced_frame.pack(fill="x", pady=(4, 0))

        exclude_similar_checkbox = ttk.Checkbutton(
            self.advanced_frame,
            text="Exclude similar characters (i, l, 1, O, 0)",
            variable=self.excludeSimilarCheck,
            onvalue=1,
            offvalue=0
        )
        exclude_similar_checkbox.pack(anchor="w", pady=(0, 8))

        hexadecimal_checkbox = ttk.Checkbutton(
            self.advanced_frame,
            text="Hexadecimal 0-9, A-F",
            variable=self.hexadecimalCheck,
            onvalue=1,
            offvalue=0
        )
        hexadecimal_checkbox.pack(anchor="w")

        score_card = ttk.Frame(outer, style="Card.TFrame", padding=18)
        score_card.pack(fill="x", padx=28, pady=(18, 0))

        score_header = ttk.Frame(score_card, style="Card.TFrame")
        score_header.pack(fill="x", pady=(0, 8))

        ttk.Label(
            score_header,
            text="Password Score",
            style="SectionTitle.TLabel"
        ).pack(side="left")

        self.score_value_label = ttk.Label(
            score_header,
            textvariable=self.score_text,
            style="FieldLabel.TLabel"
        )
        self.score_value_label.pack(side="right")

        self.score_progress = ttk.Progressbar(
            score_card,
            orient="horizontal",
            mode="determinate",
            maximum=MAX_RAW_SCORE,
            length=400,
            style="Strong.Horizontal.TProgressbar"
        )
        self.score_progress.pack(fill="x", pady=(0, 6))

        self.score_hint_label = ttk.Label(
            score_card,
            text="Weak ≤ 20   |   Weak 21–40   |   Moderate 41–60   |   Strong 61–80   |   Very-Strong 81+",
            style="Hint.TLabel",
            wraplength=760,
            justify="center"
        )
        self.score_hint_label.pack()

        suggestion_card = ttk.Frame(outer, style="Card.TFrame", padding=18)
        suggestion_card.pack(fill="x", padx=28, pady=(16, 0))

        ttk.Label(
            suggestion_card,
            text="Suggestions",
            style="SectionTitle.TLabel"
        ).pack(anchor="w", pady=(0, 8))

        self.suggestions_label = ttk.Label(
            suggestion_card,
            textvariable=self.suggestions_text,
            style="Body.TLabel",
            wraplength=760,
            justify="left"
        )
        self.suggestions_label.pack(anchor="w")

        footer_note = ttk.Label(
            outer,
            text="Tip: stronger passwords usually use longer lengths and a mix of uppercase, lowercase, numbers, and symbols.",
            style="Hint.TLabel",
            wraplength=760,
            justify="center"
        )
        footer_note.pack(pady=(16, 0))

    def toggle_advanced_settings(self):
        if self.advanced_visible:
            self.advanced_frame.pack_forget()
            self.advanced_toggle_button.config(text="Advanced Settings ▼")
            self.advanced_visible = False
        else:
            self.advanced_frame.pack(fill="x", pady=(4, 0))
            self.advanced_toggle_button.config(text="Advanced Settings ▲")
            self.advanced_visible = True

    def _apply_generation_error(self, message):
        self.password_displayed.set(message)
        self.password_label.config(bg="#c0392b")
        self.calculate_button.config(bg="#c0392b", activebackground="#c0392b", fg="white")
        self.strength_label.config(text="Invalid", fg="#c0392b")
        self.score_progress.configure(style="Weak.Horizontal.TProgressbar")
        self.score_progress["value"] = 0
        self.score_text.set("Score: 0 / 115")
        self.suggestions_text.set("Adjust the selected options and try generating again.")

    def passwordGen(self):
        chars_select = ""

        if self.hexadecimalCheck.get() == 1:
            chars_select = HEX_CHARS
            if self.excludeSimilarCheck.get() == 1:
                chars_select = "".join(ch for ch in chars_select if ch not in SIMILAR_CHARS)

            length = self.numberSelect.get()

            if not chars_select:
                self._apply_generation_error("No characters available")
                return

            pw = "".join(secrets.choice(chars_select) for _ in range(length))
        else:
            if self.lowercaseCheck.get() == 1:
                chars_select += LOWERCASE
            if self.uppercaseCheck.get() == 1:
                chars_select += UPPERCASE
            if self.digitCheck.get() == 1:
                chars_select += DIGITS
            if self.symbolCheck.get() == 1:
                chars_select += SYMBOLS

            if self.excludeSimilarCheck.get() == 1:
                chars_select = "".join(ch for ch in chars_select if ch not in SIMILAR_CHARS)

            length = self.numberSelect.get()

            if not chars_select:
                self._apply_generation_error("No character set selected")
                return

            required_groups = (
                self.lowercaseCheck.get()
                + self.uppercaseCheck.get()
                + self.digitCheck.get()
                + self.symbolCheck.get()
            )

            if length < required_groups:
                self._apply_generation_error("Length too short")
                return

            while True:
                pw = "".join(secrets.choice(chars_select) for _ in range(length))

                low_ok = (self.lowercaseCheck.get() == 0) or any(c.islower() for c in pw)
                up_ok = (self.uppercaseCheck.get() == 0) or any(c.isupper() for c in pw)
                digit_ok = (self.digitCheck.get() == 0) or any(c.isdigit() for c in pw)
                symbol_ok = (self.symbolCheck.get() == 0) or any(c in SYMBOLS for c in pw)

                if low_ok and up_ok and digit_ok and symbol_ok:
                    break

        raw_score, strength, suggestions = score_password(pw)

        if raw_score <= 20:
            color = "#c0392b"
            label_text = "Very-Weak" if raw_score <= 0 else "Weak"
            label_fg = "#c0392b"
            progress_style = "Weak.Horizontal.TProgressbar"
        elif raw_score <= 40:
            color = "#e67e22"
            label_text = "Weak"
            label_fg = "#b35d13"
            progress_style = "Medium.Horizontal.TProgressbar"
        elif raw_score <= 60:
            color = "#d4ac0d"
            label_text = "Moderate"
            label_fg = "#8a6d00"
            progress_style = "Medium.Horizontal.TProgressbar"
        elif raw_score <= 80:
            color = "#8dbb45"
            label_text = "Strong"
            label_fg = "#4d7c2a"
            progress_style = "Good.Horizontal.TProgressbar"
        else:
            color = "#5fb654"
            label_text = "Very-Strong"
            label_fg = "#2f6f3e"
            progress_style = "Strong.Horizontal.TProgressbar"

        self.password_label.config(bg=color)
        self.calculate_button.config(bg=color, activebackground=color, fg="white")
        self.strength_label.config(text=label_text, fg=label_fg)

        self.password_displayed.set(pw)

        fill_value = max(0, min(raw_score, MAX_RAW_SCORE))
        self.score_progress.configure(style=progress_style)
        self.score_progress["value"] = fill_value
        self.score_text.set(f"Score: {raw_score} / {MAX_RAW_SCORE}")

        if suggestions:
            cleaned = "• " + "".join(suggestions).replace("\n", "\n• ").strip("• ").strip()
            self.suggestions_text.set(cleaned)
        else:
            self.suggestions_text.set("No suggestions — this generated password already scores very well.")

        print("Generated Password:", pw)
        print("Raw Score:", raw_score)
        print("Strength:", strength)
        print("Suggestions:")
        print("".join(suggestions))

    def clipboardFun(self):
        current_pw = self.password_displayed.get()

        if current_pw in (
            "No character set selected",
            "Length too short",
            "Generating...",
            "No characters available"
        ):
            return

        self.controller.clipboard_clear()
        self.controller.clipboard_append(current_pw)
        self.controller.update()

    def open_save_popup(self):
        current_pw = self.password_displayed.get()

        if current_pw in (
            "No character set selected",
            "Length too short",
            "Generating...",
            "No characters available"
        ):
            messagebox.showerror("Save Error", "Generate a valid password before saving.")
            return

        popup = tk.Toplevel(self)
        popup.title("Save Password")
        popup.geometry("380x200")
        popup.resizable(False, False)
        popup.transient(self.controller)
        popup.grab_set()
        popup.configure(bg="#f4f5f7")

        container = ttk.Frame(popup, padding=20)
        container.pack(fill="both", expand=True)

        username_var = tk.StringVar()
        website_var = tk.StringVar()

        ttk.Label(container, text="Username", style="FieldLabel.TLabel").grid(
            row=0, column=0, padx=8, pady=(10, 10), sticky="w"
        )
        username_entry = ttk.Entry(container, textvariable=username_var, width=28)
        username_entry.grid(row=0, column=1, padx=8, pady=(10, 10))

        ttk.Label(container, text="Website URL", style="FieldLabel.TLabel").grid(
            row=1, column=0, padx=8, pady=10, sticky="w"
        )
        website_entry = ttk.Entry(container, textvariable=website_var, width=28)
        website_entry.grid(row=1, column=1, padx=8, pady=10)

        def submit_save():
            username = username_var.get().strip()
            website = website_var.get().strip()
            password = self.password_displayed.get()

            if not username or not website:
                messagebox.showerror("Missing Fields", "Please enter both username and website URL.")
                return

            try:
                result = save_password_record(website, username, password)

                if result == "updated":
                    messagebox.showinfo("Updated", "Existing password record updated successfully.")
                else:
                    messagebox.showinfo("Saved", "New password record saved successfully.")

                popup.destroy()
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save password:\n{e}")

        save_confirm_button = ttk.Button(
            container,
            text="Save",
            style="Primary.TButton",
            command=submit_save
        )
        save_confirm_button.grid(row=2, column=0, columnspan=2, pady=18, ipady=4)

        username_entry.focus()