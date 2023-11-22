import tkinter as tk
import cv2
from tkinter import filedialog, messagebox
from tkinter import simpledialog
import os
import string

class ImageSteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")
        self.root.geometry("250x200")
        self.label = tk.Label(root, text="Welcome :)", font=('Arial', 18),fg='#63aecb', bg='#243949')
        self.label.pack(padx=0, pady=10)
        self.root.config(bg='#243949')

        self.secret_message = ""

        self.secret_message_label = tk.Label(root, text="Enter secret message:",fg='#63aecb', bg='#243949')
        self.secret_message_label.pack()

        self.secret_message_entry = tk.Entry(root)
        self.secret_message_entry.pack()

        self.password_label = tk.Label(root, text="Enter passcode:",fg='#63aecb', bg='#243949')
        self.password_label.pack()

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt_image,bg='#63aecb', fg='#243949')
        self.encrypt_button.pack()

        self.decrypt_button = tk.Button(root, text="Decrypt", command=self.decrypt_image,bg='#63aecb', fg='#243949')
        self.decrypt_button.pack()

    def encrypt_image(self):
        try:
            img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if not img_path:
                return

            secret_message = self.secret_message_entry.get()
            self.secret_message = secret_message 
            password = self.password_entry.get()

            img = cv2.imread(img_path)

            d = {char: i for i, char in enumerate(string.printable)}

            m, n, z = 0, 0, 0

            for char in secret_message:
                img[n, m, z] = d[char]
                n, m, z = n + 1, m + 1, (z + 1) % 3

            encrypted_img_path = "encryptedImage.png"
            cv2.imwrite(encrypted_img_path, img)

            messagebox.showinfo("Encryption", f"Image encrypted and saved as '{encrypted_img_path}'")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def decrypt_image(self):
        try:
        # Ask for the encrypted image file
            encrypted_img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
            if not encrypted_img_path:
                return

        # Ask for the password used during encryption
            password = simpledialog.askstring("Password", "Enter passcode for decryption:", show='*')
            if not password:
                return

            img = cv2.imread(encrypted_img_path)

            d = {i: char for i, char in enumerate(string.printable)}

            n, m, z = 0, 0, 0
            message = ""

            for _ in range(len(self.secret_message)):
                message += d[img[n, m, z]]
                n, m, z = n + 1, m + 1, (z + 1) % 3

        # Check if the entered password matches the original password used for encryption
            if password == self.password_entry.get():
                messagebox.showinfo("Decryption", f"Decrypted message: {message}")
            else:
                messagebox.showerror("Error", "Incorrect password")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSteganographyApp(root)
    root.mainloop()