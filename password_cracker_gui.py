# GUI-based Password Cracking & Brute-Force Simulation
# Enhanced Version
# Educational Purposes Only

import tkinter as tk
from tkinter import filedialog, messagebox
import itertools
import string
import threading
import time

stop_attack = False  # Global flag to stop attack

# --- Attack Functions ---

def dictionary_attack(password, wordlist):
    for word in wordlist:
        if stop_attack:
            return False, None
        if word.strip() == password:
            return True, word.strip()
    return False, None

def brute_force_attack(password, max_length=6):
    chars = string.ascii_lowercase + string.digits  # you can add uppercase/symbols if needed
    attempts = 0
    for length in range(1, max_length+1):
        for guess in itertools.product(chars, repeat=length):
            if stop_attack:
                return False, None, attempts
            attempts += 1
            guess = ''.join(guess)
            if guess == password:
                return True, guess, attempts
    return False, None, attempts

# --- GUI Functions ---

def load_wordlist():
    path = filedialog.askopenfilename(title="Select Wordlist File")
    if path:
        wordlist_entry.delete(0, tk.END)
        wordlist_entry.insert(0, path)

def stop():
    global stop_attack
    stop_attack = True
    results_text.insert(tk.END, "\nAttack stopped by user!\n")
    print("Attack stopped by user!")

def run_attack_thread():
    threading.Thread(target=run_attack).start()

def run_attack():
    global stop_attack
    stop_attack = False

    password = password_entry.get()
    wordlist_file = wordlist_entry.get()
    max_length = int(max_length_entry.get())

    if not password:
        messagebox.showerror("Error", "Enter a password to test!")
        return

    results_text.delete("1.0", tk.END)
    results_text.insert(tk.END, f"Cracking password: {password}\n\n")
    print("Start Cracking Now...")  # Terminal message

    # Dictionary Attack
    start = time.time()
    if wordlist_file:
        try:
            with open(wordlist_file, "r", encoding="latin-1") as f:
                wordlist = f.readlines()
        except:
            messagebox.showerror("Error", "Cannot read wordlist file!")
            return
    else:
        wordlist = ["123456", "password", "admin", "pass123", "hello123"]  # default small wordlist

    success, found = dictionary_attack(password, wordlist)
    end = time.time()
    if success:
        results_text.insert(tk.END, f"[Dictionary Attack] Success! Password: {found} (Time: {end-start:.2f}s)\n")
    else:
        results_text.insert(tk.END, f"[Dictionary Attack] Failed.\n")

    # Brute-Force Attack
    start = time.time()
    success, found, attempts = brute_force_attack(password, max_length)
    end = time.time()
    if success:
        results_text.insert(tk.END, f"[Brute-Force Attack] Success! Password: {found} in {attempts} attempts (Time: {end-start:.2f}s)\n")
    else:
        if stop_attack:
            results_text.insert(tk.END, "[Brute-Force Attack] Stopped by user.\n")
        else:
            results_text.insert(tk.END, "[Brute-Force Attack] Failed.\n")

# --- GUI Layout ---

root = tk.Tk()
root.title("Cyber Password Cracking Simulator")
root.geometry("650x450")
root.configure(bg="#1b1b1b")  # Dark theme

# Title
tk.Label(root, text="Password Cracking & Brute-Force Simulation", bg="#1b1b1b", fg="lime", font=("Consolas", 16, "bold")).pack(pady=10)

# Password input
tk.Label(root, text="Password to Test:", bg="#1b1b1b", fg="white").pack(pady=5)
password_entry = tk.Entry(root, width=40, show="*", bg="#333333", fg="white", insertbackground="white")
password_entry.pack(pady=5)

# Wordlist input
tk.Label(root, text="Wordlist File (Optional):", bg="#1b1b1b", fg="white").pack(pady=5)
wordlist_entry = tk.Entry(root, width=40, bg="#333333", fg="white", insertbackground="white")
wordlist_entry.pack(pady=5)
tk.Button(root, text="Browse", command=load_wordlist, bg="#444444", fg="white").pack(pady=5)

# Max length input
tk.Label(root, text="Max Length for Brute-Force:", bg="#1b1b1b", fg="white").pack(pady=5)
max_length_entry = tk.Entry(root, width=10, bg="#333333", fg="white", insertbackground="white")
max_length_entry.insert(0, "6")  # default 6
max_length_entry.pack(pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#1b1b1b")
button_frame.pack(pady=10)

run_btn = tk.Button(button_frame, text="Run Attack", command=run_attack_thread, bg="red", fg="white", width=15)
run_btn.grid(row=0, column=0, padx=10)

stop_btn = tk.Button(button_frame, text="Stop Attack", command=stop, bg="#555555", fg="white", width=15)
stop_btn.grid(row=0, column=1, padx=10)

# Results area
results_text = tk.Text(root, height=12, width=80, bg="#222222", fg="lime", insertbackground="white")
results_text.pack(pady=10)

root.mainloop()
