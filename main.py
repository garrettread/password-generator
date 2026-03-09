import tkinter as tk
from tkinter import ttk, messagebox
from password_generator import PasswordGeneratorPage
from storage import get_decrypted_password_match
from credit_card_utils import (
    validate_credit_card,
    normalize_card_number,
    detect_card_type,
)
from credit_card_storage import save_credit_card_record


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)
        self.controller = controller

        outer = ttk.Frame(self)
        outer.pack(expand=True)

        title_label = ttk.Label(
            outer,
            text="RoboForm-Inspired Security Toolkit",
            style="Hero.TLabel"
        )
        title_label.pack(pady=(5, 8))

        subtitle_label = ttk.Label(
            outer,
            text="Generate passwords, test login autofill, and store payment data in one polished demo.",
            style="SubHero.TLabel",
            wraplength=650,
            justify="center"
        )
        subtitle_label.pack(pady=(0, 28))

        card = ttk.Frame(outer, style="Card.TFrame", padding=28)
        card.pack()

        section_title = ttk.Label(
            card,
            text="Choose an option",
            style="SectionTitle.TLabel"
        )
        section_title.pack(pady=(0, 18))

        generate_button = ttk.Button(
            card,
            text="Generate Password",
            style="Primary.TButton",
            command=lambda: controller.show_frame("PasswordGeneratorPage")
        )
        generate_button.pack(fill="x", pady=8, ipady=8)

        autofill_button = ttk.Button(
            card,
            text="Login to Website with Autofill",
            style="Primary.TButton",
            command=lambda: controller.show_frame("AutofillPage")
        )
        autofill_button.pack(fill="x", pady=8, ipady=8)

        credit_button = ttk.Button(
            card,
            text="Store Credit Card",
            style="Primary.TButton",
            command=lambda: controller.show_frame("CreditCardPage")
        )
        credit_button.pack(fill="x", pady=8, ipady=8)

        footer = ttk.Label(
            outer,
            text="Demo purposes only.",
            style="Hint.TLabel"
        )
        footer.pack(pady=(18, 0))


class AutofillPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=28)
        self.controller = controller
        self.password_visible = False

        self.website_input = tk.StringVar()
        self.login_username = tk.StringVar()
        self.login_password = tk.StringVar()

        outer = ttk.Frame(self)
        outer.pack(fill="both", expand=True)

        topbar = ttk.Frame(outer)
        topbar.pack(fill="x", pady=(0, 10))

        back_button = ttk.Button(
            topbar,
            text="← Back",
            command=self.go_back
        )
        back_button.pack(side="left")

        title = ttk.Label(
            outer,
            text="Mock Website Login with Autofill",
            style="PageTitle.TLabel"
        )
        title.pack(pady=(5, 6))

        instructions = ttk.Label(
            outer,
            text="Enter a website and username. If a saved match exists, the password will autofill automatically.",
            style="Body.TLabel",
            wraplength=700,
            justify="center"
        )
        instructions.pack(pady=(0, 20))

        card = ttk.Frame(outer, style="Card.TFrame", padding=24)
        card.pack(anchor="center")

        ttk.Label(card, text="Website", style="FieldLabel.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 12), pady=8
        )
        self.website_entry = ttk.Entry(card, textvariable=self.website_input, width=38)
        self.website_entry.grid(row=0, column=1, sticky="w", pady=8, padx=(0, 8))

        ttk.Label(card, text="Username", style="FieldLabel.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 12), pady=8
        )
        self.username_entry = ttk.Entry(card, textvariable=self.login_username, width=38)
        self.username_entry.grid(row=1, column=1, sticky="w", pady=8, padx=(0, 8))

        ttk.Label(card, text="Password", style="FieldLabel.TLabel").grid(
            row=2, column=0, sticky="w", padx=(0, 12), pady=8
        )
        self.password_entry = ttk.Entry(
            card,
            textvariable=self.login_password,
            width=38,
            show="*"
        )
        self.password_entry.grid(row=2, column=1, sticky="w", pady=8, padx=(0, 8))

        self.toggle_password_button = ttk.Button(
            card,
            text="Show",
            command=self.toggle_password_visibility,
            width=8
        )
        self.toggle_password_button.grid(row=2, column=2, sticky="w", pady=8)

        button_row = ttk.Frame(card)
        button_row.grid(row=3, column=1, columnspan=2, sticky="w", pady=(14, 0))

        autofill_button = ttk.Button(
            button_row,
            text="Autofill",
            style="Primary.TButton",
            command=self.autofill_login
        )
        autofill_button.pack(side="left", padx=(0, 10), ipady=4)

        login_button = ttk.Button(
            button_row,
            text="Login",
            command=self.mock_login
        )
        login_button.pack(side="left", ipady=4)

        hint = ttk.Label(
            outer,
            text=None,
            style="Hint.TLabel",
            wraplength=720,
            justify="center"
        )
        hint.pack(pady=(16, 0))

    def autofill_login(self):
        website = self.website_input.get().strip()
        username = self.login_username.get().strip()

        if not website:
            messagebox.showerror("Autofill Error", "Please enter a website.")
            return

        if not username:
            messagebox.showerror("Autofill Error", "Please enter a username.")
            return

        password = get_decrypted_password_match(website, username)

        if password is None:
            self.login_password.set("")
            self.password_entry.config(show="*")
            self.toggle_password_button.config(text="Show")
            self.password_visible = False
            messagebox.showerror(
                "No Match",
                "No saved password found for that website and username."
            )
            return

        self.login_password.set(password)
        messagebox.showinfo("Autofill", "Password autofilled successfully.")

    def mock_login(self):
        website = self.website_input.get().strip()
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        if not website or not username:
            messagebox.showerror("Login Error", "Website and username must be filled in.")
            return

        if not password:
            messagebox.showerror(
                "Login Error",
                "No password has been autofilled yet. Click Autofill first."
            )
            return

        messagebox.showinfo("Login", f"Mock login successful for user: {username}")

    def clear_fields(self):
        self.website_input.set("")
        self.login_username.set("")
        self.login_password.set("")
        self.password_entry.config(show="*")
        self.toggle_password_button.config(text="Show")
        self.password_visible = False

    def go_back(self):
        self.clear_fields()
        self.controller.show_frame("HomePage")

    def toggle_password_visibility(self):
        if self.password_visible:
            self.password_entry.config(show="*")
            self.toggle_password_button.config(text="Show")
            self.password_visible = False
        else:
            self.password_entry.config(show="")
            self.toggle_password_button.config(text="Hide")
            self.password_visible = True


class CreditCardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=28)
        self.controller = controller
        self.card_visible = False
        self.cvc_visible = False

        self.cardholder_var = tk.StringVar()
        self.card_number_var = tk.StringVar()
        self.expiration_var = tk.StringVar()
        self.cvc_var = tk.StringVar()
        self.card_type_var = tk.StringVar(value="Detected Type: ")
        self.card_note_var = tk.StringVar(value="")

        outer = ttk.Frame(self)
        outer.pack(fill="both", expand=True)

        topbar = ttk.Frame(outer)
        topbar.pack(fill="x", pady=(0, 10))

        back_button = ttk.Button(
            topbar,
            text="← Back",
            command=self.go_back
        )
        back_button.pack(side="left")

        title = ttk.Label(
            outer,
            text="Store Credit Card",
            style="PageTitle.TLabel"
        )
        title.pack(pady=(5, 6))

        notes_label = ttk.Label(
            outer,
            text=(
                "Use demo/test card details only.\n"
                "Accepted formats: MM/YY or MM/YYYY. Supported card types: Visa, Mastercard, American Express."
            ),
            style="Body.TLabel",
            justify="center",
            wraplength=720
        )
        notes_label.pack(pady=(0, 18))

        card = ttk.Frame(outer, style="Card.TFrame", padding=24)
        card.pack(anchor="center")

        ttk.Label(card, text="Cardholder Name", style="FieldLabel.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 14), pady=8
        )
        self.cardholder_entry = ttk.Entry(card, textvariable=self.cardholder_var, width=38)
        self.cardholder_entry.grid(row=0, column=1, sticky="w", pady=8, padx=(0, 8))

        ttk.Label(card, text="Card Number", style="FieldLabel.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 14), pady=8
        )
        self.card_number_entry = ttk.Entry(card, textvariable=self.card_number_var, width=38, show="*")
        self.card_number_entry.grid(row=1, column=1, sticky="w", pady=8, padx=(0, 8))

        self.toggle_card_button = ttk.Button(
            card,
            text="Show",
            command=self.toggle_card_visibility,
            width=8
        )
        self.toggle_card_button.grid(row=1, column=2, sticky="w", pady=8)

        ttk.Label(card, text="Expiration", style="FieldLabel.TLabel").grid(
            row=2, column=0, sticky="w", padx=(0, 14), pady=8
        )
        self.expiration_entry = ttk.Entry(card, textvariable=self.expiration_var, width=38)
        self.expiration_entry.grid(row=2, column=1, sticky="w", pady=8, padx=(0, 8))

        ttk.Label(card, text="CVC", style="FieldLabel.TLabel").grid(
            row=3, column=0, sticky="w", padx=(0, 14), pady=8
        )
        self.cvc_entry = ttk.Entry(card, textvariable=self.cvc_var, width=38, show="*")
        self.cvc_entry.grid(row=3, column=1, sticky="w", pady=8, padx=(0, 8))

        self.toggle_cvc_button = ttk.Button(
            card,
            text="Show",
            command=self.toggle_cvc_visibility,
            width=8
        )
        self.toggle_cvc_button.grid(row=3, column=2, sticky="w", pady=8)

        self.card_type_label = ttk.Label(
            card,
            textvariable=self.card_type_var,
            style="Detected.TLabel"
        )
        self.card_type_label.grid(row=4, column=1, sticky="w", pady=(8, 2))

        self.card_note_label = ttk.Label(
            card,
            textvariable=self.card_note_var,
            style="Hint.TLabel",
            wraplength=420,
            justify="left"
        )
        self.card_note_label.grid(row=5, column=1, sticky="w", pady=(0, 12))

        save_button = ttk.Button(
            card,
            text="Save Card",
            style="Primary.TButton",
            command=self.save_card
        )
        save_button.grid(row=6, column=1, sticky="w", pady=(8, 0), ipady=4)

        self.columnconfigure(0, weight=1)
        self.card_number_var.trace_add("write", self.update_card_type_live)

    def update_card_type_live(self, *args):
        raw_number = self.card_number_var.get()
        normalized_number = normalize_card_number(raw_number)

        if not normalized_number:
            self.card_type_var.set("Detected Type: ")
            self.card_note_var.set("")
            return

        if not normalized_number.isdigit():
            self.card_type_var.set("Detected Type: ")
            self.card_note_var.set("Card number should contain only digits, spaces, or dashes.")
            return

        card_type = detect_card_type(normalized_number)

        if card_type == "Visa":
            self.card_type_var.set("Detected Type: Visa")
            self.card_note_var.set("Visa usually starts with 4 and uses 13, 16, or 19 digits.")
        elif card_type == "Mastercard":
            self.card_type_var.set("Detected Type: Mastercard")
            self.card_note_var.set("Mastercard uses 16 digits and starts with 51–55 or 2221–2720.")
        elif card_type == "American Express":
            self.card_type_var.set("Detected Type: American Express")
            self.card_note_var.set("American Express uses 15 digits and a 4-digit CVC.")
        else:
            self.card_type_var.set("Detected Type: Unknown")
            self.card_note_var.set("Card type not recognized yet.")

    def save_card(self):
        cardholder = self.cardholder_var.get().strip()
        card_number = self.card_number_var.get().strip()
        expiration = self.expiration_var.get().strip()
        cvc = self.cvc_var.get().strip()

        is_valid, message, normalized_number, card_type = validate_credit_card(
            cardholder, card_number, expiration, cvc
        )

        if not is_valid:
            messagebox.showerror("Validation Error", message)
            return

        self.card_type_var.set(f"Detected Type: {card_type}")

        try:
            result, record_id = save_credit_card_record(
                cardholder,
                card_type,
                normalized_number,
                expiration,
                cvc
            )

            if result == "updated":
                messagebox.showinfo(
                    "Updated",
                    f"Existing card record updated successfully.\nID: {record_id}"
                )
            else:
                messagebox.showinfo(
                    "Saved",
                    f"New card record saved successfully.\nID: {record_id}"
                )

            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save credit card:\n{e}")

    def toggle_card_visibility(self):
        if self.card_visible:
            self.card_number_entry.config(show="*")
            self.toggle_card_button.config(text="Show")
            self.card_visible = False
        else:
            self.card_number_entry.config(show="")
            self.toggle_card_button.config(text="Hide")
            self.card_visible = True

    def toggle_cvc_visibility(self):
        if self.cvc_visible:
            self.cvc_entry.config(show="*")
            self.toggle_cvc_button.config(text="Show")
            self.cvc_visible = False
        else:
            self.cvc_entry.config(show="")
            self.toggle_cvc_button.config(text="Hide")
            self.cvc_visible = True

    def clear_fields(self):
        self.cardholder_var.set("")
        self.card_number_var.set("")
        self.expiration_var.set("")
        self.cvc_var.set("")
        self.card_type_var.set("Detected Type: ")
        self.card_note_var.set("")
        self.card_number_entry.config(show="*")
        self.toggle_card_button.config(text="Show")
        self.card_visible = False
        self.cvc_entry.config(show="*")
        self.toggle_cvc_button.config(text="Show")
        self.cvc_visible = False

    def go_back(self):
        self.clear_fields()
        self.controller.show_frame("HomePage")


class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PasswordGenerator")
        self.geometry("920x580")
        self.minsize(860, 540)

        self._setup_styles()

        container = ttk.Frame(self, padding=8)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for PageClass in (HomePage, PasswordGeneratorPage, AutofillPage, CreditCardPage):
            page_name = PageClass.__name__
            frame = PageClass(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        self.configure(bg="#f4f5f7")

        style.configure("TFrame", background="#f4f5f7")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")

        style.configure(
            "Hero.TLabel",
            background="#f4f5f7",
            foreground="#222222",
            font=("Helvetica", 24, "bold")
        )
        style.configure(
            "SubHero.TLabel",
            background="#f4f5f7",
            foreground="#5a5f69",
            font=("Helvetica", 11)
        )
        style.configure(
            "PageTitle.TLabel",
            background="#f4f5f7",
            foreground="#222222",
            font=("Helvetica", 20, "bold")
        )
        style.configure(
            "SectionTitle.TLabel",
            background="#ffffff",
            foreground="#222222",
            font=("Helvetica", 14, "bold")
        )
        style.configure(
            "Body.TLabel",
            background="#f4f5f7",
            foreground="#4f5560",
            font=("Helvetica", 11)
        )
        style.configure(
            "FieldLabel.TLabel",
            background="#ffffff",
            foreground="#222222",
            font=("Helvetica", 10, "bold")
        )
        style.configure(
            "Hint.TLabel",
            background="#f4f5f7",
            foreground="#6b7280",
            font=("Helvetica", 9)
        )
        style.configure(
            "Detected.TLabel",
            background="#ffffff",
            foreground="#2f6f3e",
            font=("Helvetica", 10, "bold")
        )

        style.configure(
            "TButton",
            font=("Helvetica", 10),
            padding=(12, 8)
        )
        style.configure(
            "Primary.TButton",
            font=("Helvetica", 10, "bold"),
            padding=(14, 9)
        )

        style.configure(
            "TEntry",
            fieldbackground="#ffffff",
            padding=6
        )

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        if page_name == "AutofillPage":
            frame.clear_fields()
        elif page_name == "CreditCardPage":
            frame.clear_fields()

        frame.tkraise()


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()