import tkinter as tk
from tkinter import ttk, messagebox
from password_generator import PasswordGeneratorPage
from storage import get_decrypted_password_match
from credit_card_utils import validate_credit_card
from credit_card_storage import save_credit_card_record


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller

        title_label = ttk.Label(
            self,
            text="Password Manager Project",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=(10, 20))

        subtitle_label = ttk.Label(
            self,
            text="Choose an option",
            font=("Helvetica", 11)
        )
        subtitle_label.pack(pady=(0, 20))

        generate_button = ttk.Button(
            self,
            text="Generate Password",
            command=lambda: controller.show_frame("PasswordGeneratorPage")
        )
        generate_button.pack(pady=8, ipadx=20, ipady=8)

        autofill_button = ttk.Button(
            self,
            text="Login to Website with Autofill",
            command=lambda: controller.show_frame("AutofillPage")
        )
        autofill_button.pack(pady=8, ipadx=20, ipady=8)

        credit_button = ttk.Button(
            self,
            text="Store Credit Card",
            command=lambda: controller.show_frame("CreditCardPage")
        )
        credit_button.pack(pady=8, ipadx=20, ipady=8)


class AutofillPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        self.controller = controller
        self.password_visible = False

        self.website_input = tk.StringVar()
        self.login_username = tk.StringVar()
        self.login_password = tk.StringVar()

        title = ttk.Label(
            self,
            text="Mock Website Login with Autofill",
            font=("Helvetica", 16, "bold")
        )
        title.grid(row=0, column=0, columnspan=3, pady=(5, 20))

        instructions = ttk.Label(
            self,
            text="Enter a website and username. If a saved match exists, the password will autofill."
        )
        instructions.grid(row=1, column=0, columnspan=3, pady=(0, 15))

        ttk.Label(self, text="Website:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.website_entry = ttk.Entry(self, textvariable=self.website_input, width=32)
        self.website_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self, text="Username:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = ttk.Entry(self, textvariable=self.login_username, width=32)
        self.username_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self, text="Password:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = ttk.Entry(
            self,
            textvariable=self.login_password,
            width=32,
            show="*"
        )
        self.password_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.toggle_password_button = ttk.Button(
            self,
            text="Show",
            command=self.toggle_password_visibility,
            width=8
        )
        self.toggle_password_button.grid(row=4, column=2, padx=5, pady=5, sticky="w")

        autofill_button = ttk.Button(
            self,
            text="Autofill",
            command=self.autofill_login
        )
        autofill_button.grid(row=5, column=1, pady=(10, 10), sticky="w")

        login_button = ttk.Button(
            self,
            text="Login",
            command=self.mock_login
        )
        login_button.grid(row=6, column=1, pady=10, sticky="w")

        back_button = ttk.Button(
            self,
            text="Back",
            command=self.go_back
        )
        back_button.grid(row=7, column=0, pady=15, sticky="w")

        self.columnconfigure(1, weight=1)

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
        super().__init__(parent, padding=20)
        self.controller = controller
        self.card_visible = False
        self.cvc_visible = False

        self.cardholder_var = tk.StringVar()
        self.card_number_var = tk.StringVar()
        self.expiration_var = tk.StringVar()
        self.cvc_var = tk.StringVar()
        self.card_type_var = tk.StringVar(value="Detected Type: ")
        self.card_note_var = tk.StringVar(value="")

        title = ttk.Label(
            self,
            text="Store Credit Card",
            font=("Helvetica", 16, "bold")
        )
        title.grid(row=0, column=0, columnspan=4, pady=(5, 20))

        notes_label = ttk.Label(
            self,
            text=(
                "Formatting Notes:\n"
                "- Card number must be a valid Visa, Mastercard, or American Express number\n"
                "- Expiration must be MM/YY or MM/YYYY and cannot be expired\n"
                "- CVC must be 3 digits for Visa/Mastercard or 4 digits for AmEx"
            ),
            justify="left"
        )
        notes_label.grid(row=1, column=0, columnspan=4, sticky="w", padx=5, pady=(0, 15))

        ttk.Label(self, text="Cardholder Name:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.cardholder_entry = ttk.Entry(self, textvariable=self.cardholder_var, width=34)
        self.cardholder_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self, text="Card Number:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.card_number_entry = ttk.Entry(self, textvariable=self.card_number_var, width=34, show="*")
        self.card_number_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.toggle_card_button = ttk.Button(
            self,
            text="Show",
            command=self.toggle_card_visibility,
            width=8
        )
        self.toggle_card_button.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        ttk.Label(self, text="Expiration:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.expiration_entry = ttk.Entry(self, textvariable=self.expiration_var, width=34)
        self.expiration_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self, text="CVC:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.cvc_entry = ttk.Entry(self, textvariable=self.cvc_var, width=34, show="*")
        self.cvc_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.toggle_cvc_button = ttk.Button(
            self,
            text="Show",
            command=self.toggle_cvc_visibility,
            width=8
        )
        self.toggle_cvc_button.grid(row=5, column=2, padx=5, pady=5, sticky="w")

        self.card_type_label = ttk.Label(self, textvariable=self.card_type_var, font=("Helvetica", 10, "bold"))
        self.card_type_label.grid(row=6, column=1, sticky="w", padx=5, pady=(5, 2))

        self.card_note_label = ttk.Label(self, textvariable=self.card_note_var, foreground="gray")
        self.card_note_label.grid(row=7, column=1, sticky="w", padx=5, pady=(0, 10))

        save_button = ttk.Button(
            self,
            text="Save Card",
            command=self.save_card
        )
        save_button.grid(row=8, column=1, pady=(10, 10), sticky="w")

        back_button = ttk.Button(
            self,
            text="Back",
            command=self.go_back
        )
        back_button.grid(row=9, column=0, pady=15, sticky="w")

        self.columnconfigure(1, weight=1)

        # Live detection while typing
        self.card_number_var.trace_add("write", self.update_card_type_live)

    def update_card_type_live(self, *args):
        from credit_card_utils import normalize_card_number, detect_card_type

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
            self.card_note_var.set("Mastercard uses 16 digits and starts with 51-55 or 2221-2720.")
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
        self.geometry("850x480")

        container = ttk.Frame(self)
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