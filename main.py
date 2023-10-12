from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)
    password = ""

    for char in password_list:
        password += char

    password_value.set(password)
    pyperclip.copy(password)
    
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    username = ent_email.get()
    password = ent_password.get()
    website = ent_website.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }
    
    if website == "" or password == "" or username == "":
        messagebox.showinfo(title="Oops", message=f"Please don't leave any fields empty!")
    else:
        try: 
            with open("data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)

        except FileNotFoundError:
            messagebox.showinfo(title="Notification", message=f"File not found, creating new file.")
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
              
        else:
            #Updating old data with new data
            data.update(new_data)       
       
            with open("data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:    
            website_value.set("")
            password_value.set("")

# -------------------------- FIND PASSWORD ---------------------------- #
def find_password():
    website = ent_website.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No record of {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(85, 100, image=logo_img)
canvas.grid(row=0, column=1)

lbl_website = Label(text="Website:")
lbl_website.grid(row=1, column=0)

lbl_username = Label(text="Email/Username:")
lbl_username.grid(row=2, column=0)

lbl_password = Label(text="Password:")
lbl_password.grid(row=3, column=0)

website_value = StringVar()
ent_website = Entry(width=30, textvariable=website_value)
ent_website.grid(row=1, column=1, columnspan=2, sticky="w")

ent_email = Entry(width=30)
ent_email.insert(0, string="joshuabearne@gmail.com")
ent_email.grid(row=2, column=1, columnspan=2, sticky="w")

password_value = StringVar()
ent_password = Entry(width=30, textvariable=password_value, show="*")
ent_password.grid(row=3, column=1, sticky="w")

btn_gen_password = Button(text="Generate", command=password_generator)
btn_gen_password.grid(row=3, column=2, sticky="w")

btn_add = Button(text="Add", width=25, command=save, bg="light blue")
btn_add.grid(row=4, column=1, columnspan=2, sticky="w")

btn_search = Button(text="Search", command=find_password)
btn_search.grid(row=1, column=2, sticky="w")

window.mainloop()