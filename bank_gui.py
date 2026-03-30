import pyodbc
import tkinter as tk
from tkinter import messagebox

# ================= DB CONNECTION =================
conn = pyodbc.connect('DSN=bank_db_dsn;UID=root;PWD=ngp@2007')
cursor = conn.cursor()

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Bank Management System")
root.geometry("500x450")
root.configure(bg="#e6f2ff")

# ================= FRAME SYSTEM =================
container = tk.Frame(root)
container.pack(fill="both", expand=True)

frames = {}

def show_frame(name):
    frames[name].tkraise()

# ================= FUNCTIONS =================

def create_account():
    try:
        cursor.execute("INSERT INTO accounts VALUES (?, ?, ?)",
                       (acc_entry.get(), name_entry.get(), bal_entry.get()))
        conn.commit()
        messagebox.showinfo("Success", "Account Created!")
    except:
        messagebox.showerror("Error", "Account Exists!")

def deposit():
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_no=?",
                   (amt_entry.get(), acc_entry2.get()))
    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Account not found")
    else:
        conn.commit()
        messagebox.showinfo("Success", "Deposited!")

def withdraw():
    cursor.execute("SELECT balance FROM accounts WHERE account_no=?",
                   (acc_entry3.get(),))
    row = cursor.fetchone()

    if row and row[0] >= float(amt_entry2.get()):
        cursor.execute("UPDATE accounts SET balance=balance-? WHERE account_no=?",
                       (amt_entry2.get(), acc_entry3.get()))
        conn.commit()
        messagebox.showinfo("Success", "Withdrawn!")
    else:
        messagebox.showerror("Error", "Invalid operation")

def check_balance():
    cursor.execute("SELECT * FROM accounts WHERE account_no=?",
                   (acc_entry4.get(),))
    row = cursor.fetchone()

    if row:
        messagebox.showinfo("Details", f"Name: {row[1]}\nBalance: {row[2]}")
    else:
        messagebox.showerror("Error", "Not found")

# ================= CREATE FRAMES =================
for name in ["Home", "Create", "Deposit", "Withdraw", "Balance"]:
    frame = tk.Frame(container, bg="#e6f2ff")
    frames[name] = frame
    frame.grid(row=0, column=0, sticky="nsew")

# ================= HOME =================
home = frames["Home"]

tk.Label(home, text="🏦 Bank Management System",
         font=("Arial", 18, "bold"),
         bg="#e6f2ff").pack(pady=30)

tk.Button(home, text="Create Account", width=20,
          command=lambda: show_frame("Create")).pack(pady=8)

tk.Button(home, text="Deposit", width=20,
          command=lambda: show_frame("Deposit")).pack(pady=8)

tk.Button(home, text="Withdraw", width=20,
          command=lambda: show_frame("Withdraw")).pack(pady=8)

tk.Button(home, text="Check Balance", width=20,
          command=lambda: show_frame("Balance")).pack(pady=8)

# ================= CREATE PAGE =================
create = frames["Create"]

tk.Label(create, text="Create Account",
         font=("Arial", 16), bg="#e6f2ff").pack(pady=10)

tk.Label(create, text="Account Number").pack()
acc_entry = tk.Entry(create)
acc_entry.pack()

tk.Label(create, text="Name").pack()
name_entry = tk.Entry(create)
name_entry.pack()

tk.Label(create, text="Balance").pack()
bal_entry = tk.Entry(create)
bal_entry.pack()

tk.Button(create, text="Submit", command=create_account).pack(pady=10)
tk.Button(create, text="Back", command=lambda: show_frame("Home")).pack()

# ================= DEPOSIT PAGE =================
deposit_f = frames["Deposit"]

tk.Label(deposit_f, text="Deposit",
         font=("Arial", 16), bg="#e6f2ff").pack(pady=10)

tk.Label(deposit_f, text="Account Number").pack()
acc_entry2 = tk.Entry(deposit_f)
acc_entry2.pack()

tk.Label(deposit_f, text="Amount").pack()
amt_entry = tk.Entry(deposit_f)
amt_entry.pack()

tk.Button(deposit_f, text="Deposit", command=deposit).pack(pady=10)
tk.Button(deposit_f, text="Back", command=lambda: show_frame("Home")).pack()

# ================= WITHDRAW PAGE =================
withdraw_f = frames["Withdraw"]

tk.Label(withdraw_f, text="Withdraw",
         font=("Arial", 16), bg="#e6f2ff").pack(pady=10)

tk.Label(withdraw_f, text="Account Number").pack()
acc_entry3 = tk.Entry(withdraw_f)
acc_entry3.pack()

tk.Label(withdraw_f, text="Amount").pack()
amt_entry2 = tk.Entry(withdraw_f)
amt_entry2.pack()

tk.Button(withdraw_f, text="Withdraw", command=withdraw).pack(pady=10)
tk.Button(withdraw_f, text="Back", command=lambda: show_frame("Home")).pack()

# ================= BALANCE PAGE =================
balance_f = frames["Balance"]

tk.Label(balance_f, text="Check Balance",
         font=("Arial", 16), bg="#e6f2ff").pack(pady=10)

tk.Label(balance_f, text="Account Number").pack()
acc_entry4 = tk.Entry(balance_f)
acc_entry4.pack()

tk.Button(balance_f, text="Check", command=check_balance).pack(pady=10)
tk.Button(balance_f, text="Back", command=lambda: show_frame("Home")).pack()

# ================= START =================
show_frame("Home")

root.mainloop()