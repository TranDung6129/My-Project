from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_entry.delete(0, END)
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for char in range(nr_symbols)]
    password_list += [random.choice(numbers) for char in range(nr_numbers)]

    random.shuffle(password_list)

    password_generated = "".join(password_list)
    password_entry.insert(0, password_generated)
    pyperclip.copy(password_generated)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_box_entry.get()
    password = password_entry.get()
    email = email_username_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oop", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_box_entry.delete(0, END)
            password_entry.delete(0, END)


# ------------------------ SEARCH PASSWORD -----------------------------#
def find_password():
    website = website_box_entry.get()
    email = email_username_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found!")
    else:
        if website in data:
            messagebox.showinfo(title=website,
                                message=f"Email: {data[website]['email']}\nPassword: {data[website]['password']}")
        else:
            messagebox.showwarning(title=website, message=f"No details for the {website} exists!")
# ---------------------------- UI SETUP ------------------------------- #

# Setup Window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Setup canvas
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Website input
website_box = Label(text="Website:")
website_box.grid(column=0, row=1)

website_box_entry = Entry(width=33)
website_box_entry.grid(column=1, row=1)
website_box_entry.focus()

# Email/Username input
email_username = Label(text="Email/Username:")
email_username.grid(column=0, row=2)

email_username_entry = Entry(width=52)
email_username_entry.grid(column=1, row=2, columnspan=2)

email_username_entry.insert(0, "dung2002lca1@gmail.com")
# Password input
password = Label(text="Password:")
password.grid(column=0, row=3)

password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

# Generate Password button
gen_pass = Button(text="Generate Password", command=generate_password)
gen_pass.grid(column=2, row=3)

# Add button
add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)

# Search button
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
