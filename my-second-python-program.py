"""
Password Manager - Single File
Requires: pyperclip (optional: pip install pyperclip)
"""
import json, random, string
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

try:
    import pyperclip
except ImportError:
    pyperclip = None

DB = Path("passwords.json")

def load():
    if DB.exists():
        return json.loads(DB.read_text())
    return {}

def save_db(data):
    DB.write_text(json.dumps(data, indent=4))

def generate():
    chars = string.ascii_letters + string.digits + "!@#$%^&*?"
    pw = "".join(random.choice(chars) for _ in range(16))
    password.delete(0, tk.END)
    password.insert(0, pw)
    if pyperclip:
        pyperclip.copy(pw)

def save():
    w,e,p = website.get().strip(), email.get().strip(), password.get().strip()
    if not (w and e and p):
        messagebox.showwarning("Missing","Fill all fields")
        return
    data = load()
    data[w] = {"email":e,"password":p}
    save_db(data)
    messagebox.showinfo("Saved","Credentials saved.")
    website.delete(0,tk.END)
    password.delete(0,tk.END)

def search():
    w=website.get().strip()
    data=load()
    if w in data:
        d=data[w]
        messagebox.showinfo("Found",f"Email: {d['email']}\nPassword: {d['password']}")
    else:
        messagebox.showinfo("Not Found","No entry.")

root=tk.Tk()
root.title("Password Manager")
for i,t in enumerate(["Website","Email","Password"]):
    tk.Label(root,text=t).grid(row=i,column=0,padx=5,pady=5,sticky="e")
website=tk.Entry(root,width=35); website.grid(row=0,column=1)
email=tk.Entry(root,width=35); email.grid(row=1,column=1)
password=tk.Entry(root,width=22); password.grid(row=2,column=1,sticky="w")
tk.Button(root,text="Search",command=search).grid(row=0,column=2,padx=5)
tk.Button(root,text="Generate",command=generate).grid(row=2,column=2,padx=5)
tk.Button(root,text="Save",command=save,width=30).grid(row=3,column=1,pady=10)
root.mainloop()
