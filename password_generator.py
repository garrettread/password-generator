import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox
from storage import save_password_record
from password_checker_connector import score_password, display_score

# Character sets
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = string.punctuation


class PasswordGeneratorPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=(3, 3, 3, 3))
        self.controller = controller

        # Tkinter variables
        self.lowercaseCheck = tk.IntVar(value=1)
        self.uppercaseCheck = tk.IntVar(value=1)
        self.digitCheck = tk.IntVar(value=1)
        self.symbolCheck = tk.IntVar(value=1)
        self.numberSelect = tk.IntVar(value=16)
        self.password_displayed = tk.StringVar(value="Generating...")

        self._build_ui()

        # Generate one password when page loads
        self.after(1, self.passwordGen)

    def _build_ui(self):
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Title
        title_label = ttk.Label(
            self,
            text="Random Password Generator",
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(column=2, row=1, columnspan=4, sticky=tk.N)
        title_label["padding"] = 10

        # Strength label
        self.strength_label = tk.Label(
            self,
            text="",
            font=("Helvetica", 12, "bold"),
            bg=self.controller.cget("bg")
        )
        self.strength_label.grid(column=2, row=2, columnspan=4, sticky=tk.N, padx=10, pady=5)

        # Checkboxes
        upper_checkbox = ttk.Checkbutton(
            self, text="A - Z", variable=self.uppercaseCheck, onvalue=1, offvalue=0
        )
        upper_checkbox.grid(column=2, row=4, sticky=tk.NW)
        upper_checkbox["padding"] = 4

        lower_checkbox = ttk.Checkbutton(
            self, text="a - z", variable=self.lowercaseCheck, onvalue=1, offvalue=0
        )
        lower_checkbox.grid(column=3, row=4, sticky=tk.NW)
        lower_checkbox["padding"] = 4

        digit_checkbox = ttk.Checkbutton(
            self, text="0 - 9", variable=self.digitCheck, onvalue=1, offvalue=0
        )
        digit_checkbox.grid(column=4, row=4, sticky=tk.NW)
        digit_checkbox["padding"] = 4

        symbol_checkbox = ttk.Checkbutton(
            self, text="symbol", variable=self.symbolCheck, onvalue=1, offvalue=0
        )
        symbol_checkbox.grid(column=5, row=4, sticky=tk.NW)
        symbol_checkbox["padding"] = 4

        # Length spinbox
        spin_number = ttk.Spinbox(
            self, from_=1, to=512, textvariable=self.numberSelect, width=4
        )
        spin_number.grid(column=1, row=3, sticky=tk.E)

        # Password display
        self.password_label = tk.Label(
            self,
            textvariable=self.password_displayed,
            width=32,
            fg="white",
            bg="darkgreen",
            font=("Helvetica", 10, "normal"),
            anchor="w",
            padx=8
        )
        self.password_label.grid(column=2, row=3, columnspan=3, sticky=tk.EW, ipady=5)

        # Generate button
        self.calculate_button = tk.Button(
            self,
            text="Generate",
            command=self.passwordGen,
            relief="sunken",
            borderwidth=0,
            activeforeground="white",
            bg="darkgreen",
            fg="white",
            activebackground="darkgreen"
        )
        self.calculate_button.grid(column=5, row=3, sticky=tk.W, ipady=1)

        # Copy button
        clip_frame = tk.Frame(self, highlightbackground="green", highlightthickness=1)
        clip_frame.grid(column=6, row=3, padx=4, pady=4, ipadx=1, ipady=1)

        clip_button = tk.Button(
            clip_frame,
            text="Copy",
            command=self.clipboardFun,
            relief="sunken",
            borderwidth=0
        )
        clip_button.pack(fill="both", expand=True, padx=2, pady=2)

        # Save button
        save_button = ttk.Button(
            self,
            text="Save",
            command=self.open_save_popup
        )
        save_button.grid(column=6, row=4, sticky=tk.E, padx=4, pady=4)

        # Back button
        back_button = ttk.Button(
            self,
            text="Back",
            command=lambda: self.controller.show_frame("HomePage")
        )
        back_button.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

        # Layout config
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=3)
        self.columnconfigure(4, weight=3)
        self.columnconfigure(5, weight=0)
        self.columnconfigure(6, weight=0)

    def passwordGen(self):
        chars_select = ""

        # Build selected character pool
        if self.lowercaseCheck.get() == 1:
            chars_select += LOWERCASE
        if self.uppercaseCheck.get() == 1:
            chars_select += UPPERCASE
        if self.digitCheck.get() == 1:
            chars_select += DIGITS
        if self.symbolCheck.get() == 1:
            chars_select += SYMBOLS

        length = self.numberSelect.get()

        # No checkbox selected
        if not chars_select:
            self.password_displayed.set("No character set selected")
            self.password_label.config(bg="red")
            self.calculate_button.config(bg="red", activebackground="red", fg="white")
            self.strength_label.config(text="SELECT OPTIONS", fg="red")
            return

        # Count required groups
        required_groups = (
            self.lowercaseCheck.get()
            + self.uppercaseCheck.get()
            + self.digitCheck.get()
            + self.symbolCheck.get()
        )

        # Impossible length
        if length < required_groups:
            self.password_displayed.set("Length too short")
            self.password_label.config(bg="red")
            self.calculate_button.config(bg="red", activebackground="red", fg="white")
            self.strength_label.config(text="LENGTH TOO SHORT", fg="red")
            return

        # Generate until it satisfies selected options
        while True:
            pw = "".join(secrets.choice(chars_select) for _ in range(length))

            low_ok = (self.lowercaseCheck.get() == 0) or any(c.islower() for c in pw)
            up_ok = (self.uppercaseCheck.get() == 0) or any(c.isupper() for c in pw)
            digit_ok = (self.digitCheck.get() == 0) or any(c.isdigit() for c in pw)
            symbol_ok = (self.symbolCheck.get() == 0) or any(c in SYMBOLS for c in pw)

            if low_ok and up_ok and digit_ok and symbol_ok:
                break

        # Score password
        raw_score, strength, suggestions = score_password(pw)
        score_for_ui = display_score(raw_score)

        # Update UI colors
        if score_for_ui <= 25:
            color = "red"
            label_text = "WEAK"
        elif score_for_ui <= 50:
            color = "orange"
            label_text = "MEDIUM"
        elif score_for_ui <= 75:
            color = "yellowgreen"
            label_text = "GOOD"
        else:
            color = "darkgreen"
            label_text = "STRONG"

        self.password_label.config(bg=color)
        self.calculate_button.config(bg=color, activebackground=color, fg="white")
        self.strength_label.config(text=label_text, fg="black")

        self.password_displayed.set(pw)

        # Optional console output for debugging
        print("Generated Password:", pw)
        print("Score:", score_for_ui)
        print("Strength:", strength)
        print("Suggestions:")
        print("".join(suggestions))

    def clipboardFun(self):
        current_pw = self.password_displayed.get()

        # Don't copy error/status text
        if current_pw in ("No character set selected", "Length too short", "Generating..."):
            return

        self.controller.clipboard_clear()
        self.controller.clipboard_append(current_pw)
        self.controller.update()

    def open_save_popup(self):
        current_pw = self.password_displayed.get()

        # Prevent saving invalid/status text
        if current_pw in ("No character set selected", "Length too short", "Generating..."):
            messagebox.showerror("Save Error", "Generate a valid password before saving.")
            return

        popup = tk.Toplevel(self)
        popup.title("Save Password")
        popup.geometry("350x180")
        popup.resizable(False, False)
        popup.transient(self.controller)
        popup.grab_set()

        username_var = tk.StringVar()
        website_var = tk.StringVar()

        ttk.Label(popup, text="Username:").grid(row=0, column=0, padx=10, pady=(15, 8), sticky="w")
        username_entry = ttk.Entry(popup, textvariable=username_var, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=(15, 8))

        ttk.Label(popup, text="Website URL:").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        website_entry = ttk.Entry(popup, textvariable=website_var, width=30)
        website_entry.grid(row=1, column=1, padx=10, pady=8)

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

        save_confirm_button = ttk.Button(popup, text="Save", command=submit_save)
        save_confirm_button.grid(row=2, column=0, columnspan=2, pady=15)

        username_entry.focus()