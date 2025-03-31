import os 
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import base64
import secrets

# Generate key from password
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())

# Encrypt file
def encrypt_file(file_path, password):
    salt = secrets.token_bytes(16)  # Generate a random salt
    key = derive_key(password, salt)
    iv = secrets.token_bytes(16)  # Generate a random IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    with open(file_path, 'rb') as f:
        plaintext = f.read()
    
    padding_length = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_length]) * padding_length  # Add PKCS7 padding
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(salt + iv + ciphertext)
    
    messagebox.showinfo("Success", f"File encrypted and saved as: {encrypted_file_path}")

# Decrypt file
def decrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    salt, iv, ciphertext = data[:16], data[16:32], data[32:]
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]  # Remove padding
    
    decrypted_file_path = file_path.replace(".enc", "_decrypted")
    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)
    
    messagebox.showinfo("Success", f"File decrypted and saved as: {decrypted_file_path}")

# GUI Functions
def select_file():
    file_path = filedialog.askopenfilename()
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

def encrypt_action():
    file_path = entry_file.get()
    password = entry_password.get()
    if file_path and password:
        encrypt_file(file_path, password)
    else:
        messagebox.showerror("Error", "Please select a file and enter a password.")

def decrypt_action():
    file_path = entry_file.get()
    password = entry_password.get()
    if file_path and password:
        decrypt_file(file_path, password)
    else:
        messagebox.showerror("Error", "Please select a file and enter a password.")

# Tkinter UI Setup
root = tk.Tk()
root.title("AES-256 File Encryption")
root.geometry("800x600")  # Full-length window
root.configure(bg="black")

frame = tk.Frame(root, bg="black")
frame.place(relx=0.5, rely=0.5, anchor="center")  # Centering the frame

style = {
    "bg": "black",
    "fg": "white",
    "font": ("Arial", 12)
}

def add_spacing(widget):
    widget.pack(pady=10)  # Increased spacing between fields

tk.Label(frame, text="Select File:", **style).pack()
entry_file = tk.Entry(frame, width=50, bd=2, relief="solid", highlightbackground="blue", highlightthickness=2)
add_spacing(entry_file)
tk.Button(frame, text="Browse", command=select_file, bg="aqua", fg="black", font=("Arial", 12, "bold")).pack(pady=10)

tk.Label(frame, text="Enter Password:", **style).pack()
entry_password = tk.Entry(frame, show="*", width=50, bd=2, relief="solid", highlightbackground="blue", highlightthickness=2)
add_spacing(entry_password)

tk.Button(frame, text="Encrypt", command=encrypt_action, bg="aqua", fg="black", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(frame, text="Decrypt", command=decrypt_action, bg="aqua", fg="black", font=("Arial", 12, "bold")).pack(pady=10)

root.mainloop()
