import secrets
import string
from tkinter import *
from tkinter import ttk
from password_checker_connector import score_password, display_score

# Character sets
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
symbols = string.punctuation

#password set defaults
chars_select = lowercase+uppercase+digits+symbols
length = 16

#Password Generator Function
#also changes password/strength labels depending on evaluated password strength
def passwordGen():
    chars_select = ''

    #add selected sets to password set
    if lowercaseCheck.get() == 1:
        chars_select += lowercase
    if uppercaseCheck.get() == 1:
        chars_select += uppercase
    if digitCheck.get() == 1:
        chars_select += digits
    if symbolCheck.get() == 1:
        chars_select += symbols

    # Password length (RoboForm default-ish) to fix later
    length = numberSelect.get()

    # Generate secure password
    #adds check that it statisfies user inputs (1 upper char, 1 lower char, 1 digit, 1 special char)

    while True:
        pw = ''.join(secrets.choice(chars_select) for _ in range(length))
        lowCheck = lowercaseCheck.get()
        upCheck = uppercaseCheck.get()
        dCheck = digitCheck.get()
        symCheck = symbolCheck.get()
        exitCheck1 = True
        exitCheck2 = True
        exitCheck3 = True
        exitCheck4 = True

        if(length >= 4):
            if (lowCheck == 1):
                if(any(c.islower() for c in pw)):
                    exitCheck1 = True
                else:
                    exitCheck1 = False

            if(upCheck == 1):
                if(any(c.isupper() for c in pw)):
                    exitCheck2 = True
                else:
                    exitCheck2 = False

            if(dCheck == 1):
                if(sum(c.isdigit() for c in pw) >= 1):
                    exitCheck3 = True
                else:
                    exitCheck3 = False
            
            if(symCheck == 1):
                if(any(c in symbols for c in pw)):
                    exitCheck4 = True
                else:
                    exitCheck4 = False

        if(exitCheck1 == True and exitCheck2 == True and exitCheck3 == True and exitCheck4 == True):
            break

    #pw = ''.join(secrets.choice(chars_select) for _ in range(length))

    print("Generated Password:", pw)

    # Send password to checker
    raw_score, strength, suggestions = score_password(pw)

    score_for_ui = display_score(raw_score)

    if(score_for_ui <= 25):
        password_label.config(background="red")
        calculate_button.config(background="red", activebackground="red", foreground='white')
        strength_label.config(text="WEAK")
    elif(score_for_ui <= 50):
        password_label.config(background="orange")
        calculate_button.config(background="orange", activebackground="orange", foreground='white')
        strength_label.config(text="MEDIUM")
    elif(score_for_ui <= 75):
        password_label.config(background="yellowgreen")
        calculate_button.config(background="yellowgreen", activebackground="yellowgreen", foreground='white')
        strength_label.config(text="GOOD")
    else:
        password_label.config(background="darkgreen")
        calculate_button.config(background="darkgreen", activebackground="darkgreen", foreground='white')
        strength_label.config(text="STRONG")

    print("Score:", score_for_ui)
    print("Strength:", strength)
    print("Suggestions:")
    print("".join(suggestions))

    password_displayed.set(pw)

#clears clipboard, then fills it with password
def clipboardFun():
    root.clipboard_clear()
    root.clipboard_append(password_displayed.get())

#----------GUI elements---------
#GUI window
root = Tk()
root.title("PasswordGenerator")
root.geometry("650x200")

#all GUI elements attach to this frame, rather than the base window
mainframe = ttk.Frame(root, padding=(3, 3, 3, 3))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

#Title label
title_label = ttk.Label(mainframe, text="Random Password Generator", font=("Helvetica", 16, "bold"))
title_label.grid(column=2, row=1, columnspan=4, sticky=(N))
title_label['padding'] = 10

#description label? (Generate strong, random, and unique passwords with the click of a button) maybe?

#Strength display (with color)
#make image thing? use images from source example?
strength_label = ttk.Label(mainframe, text="", font=("Helvetica", 12, "bold"))
strength_label.grid(column=2, row=2, columnspan=4, sticky=N, padx=10, pady=5)

#Checkbox vars(holds value related to state of checkbox)
lowercaseCheck = IntVar(value=1)
uppercaseCheck = IntVar(value=1)
digitCheck = IntVar(value=1)
symbolCheck = IntVar(value=1)

#Checkbutton wigits
upper_checkbox = ttk.Checkbutton(mainframe, text="A - Z", variable=uppercaseCheck, onvalue=1, offvalue=0)
upper_checkbox.grid(column=2, row=4, sticky=NW)
upper_checkbox['padding'] = 4
lower_checkbox = ttk.Checkbutton(mainframe, text="a - z", variable=lowercaseCheck, onvalue=1, offvalue=0)
lower_checkbox.grid(column=3, row=4, sticky=NW)
lower_checkbox['padding'] = 4
digit_checkbox = ttk.Checkbutton(mainframe, text="0 - 9", variable=digitCheck, onvalue=1, offvalue=0)
digit_checkbox.grid(column=4, row=4, sticky=NW)
digit_checkbox['padding'] = 4
symbol_checkbox = ttk.Checkbutton(mainframe, text="symbol", variable=symbolCheck, onvalue=1, offvalue=0)
symbol_checkbox.grid(column=5, row=4, sticky=NW)
symbol_checkbox['padding'] = 4

#Number spinbox var
numberSelect = IntVar(value=16)

#Number spinbox (RoboForm allows up to 512 length passwords)
spin_number = ttk.Spinbox(mainframe, from_=1, to=512, textvariable=numberSelect, width=4)
spin_number.grid(column=1, row=3, sticky=E)

#Password Label/Password display
password_displayed = StringVar()
password_label = ttk.Label(mainframe, textvariable=password_displayed, width=26, foreground="white", font=("Helvetica", 10, "normal"))
password_label.grid(column=2, row=3, columnspan=4, sticky=EW, ipady=5)
#password_label['padding'] = 4

#Calculate button
calculate_button = Button(mainframe, text="Generate", command=passwordGen, relief="sunken", borderwidth=0, activeforeground="white")
calculate_button.grid(column=5, row=3, sticky=W, ipady=1)

clip_frame = Frame(mainframe, highlightbackground="green", highlightcolor="red", highlightthickness=1)
clip_frame.grid(column=6, row=3, padx=4, pady=4, ipadx=1, ipady=1)

#clipboard wigit
clip_button = Button(clip_frame, text="Copy", command=clipboardFun, relief='sunken', borderwidth=0, activeforeground="green")
clip_button.pack(fill='both', expand=True, padx=2, pady=2)

#GUI configuration (for resizing window/padding)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)	
mainframe.columnconfigure(1, weight=0)
mainframe.columnconfigure(2, weight=3)
mainframe.columnconfigure(3, weight=3)
mainframe.columnconfigure(4, weight=3)
mainframe.columnconfigure(5, weight=0)
mainframe.columnconfigure(6, weight=0)

#Fills box with generated password on opening window
root.after(1, passwordGen)

root.mainloop()