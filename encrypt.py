import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import os
from cryptography.fernet import Fernet
import hashlib
import base64

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encoding - Programmer Theme")
        self.root.geometry("600x400")
        self.root.configure(bg="#282c34")  # Dark gray background
        
        self.img_path = None
        self.char_to_int = {chr(i): i for i in range(255)}
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme
        self.style.configure('Custom.TFrame', background='#282c34')
        self.style.configure('Custom.TButton', padding=10, font=('Consolas', 12), background="#61dafb", foreground="#282c34")
        self.style.configure('Custom.TLabel', background="#282c34", foreground="#61dafb", font=('Consolas', 12))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root, style='Custom.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ttk.Frame(main_container, style='Custom.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(title_frame, text="Image Encoding", 
                         font=("Consolas", 20, "bold"), bg="#282c34", fg="#61dafb")
        title.pack()
        
        # Image selection section
        img_frame = tk.LabelFrame(main_container, text="Image Selection", 
                                  font=("Consolas", 12, "bold"), bg="#282c34", fg="#61dafb", 
                                  padx=10, pady=10)
        img_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.img_path_label = tk.Label(img_frame, text="No image selected", 
                                       bg="#282c34", fg="#abb2bf", wraplength=300)
        self.img_path_label.pack(fill=tk.X, pady=(0, 5))
        
        select_btn = tk.Button(img_frame, text="Select Image", command=self.select_image, 
                               bg="#61dafb", fg="#282c34", font=("Consolas", 11), padx=20, pady=5)
        select_btn.pack()
        
        # Message input section
        msg_frame = tk.LabelFrame(main_container, text="Message Input", 
                                  font=("Consolas", 12, "bold"), bg="#282c34", fg="#61dafb", 
                                  padx=10, pady=10)
        msg_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.msg_entry = tk.Text(msg_frame, width=40, height=4, font=("Consolas", 11), wrap=tk.WORD, bg="#21252b", fg="#61dafb", insertbackground="#61dafb")
        self.msg_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Password section
        pass_frame = tk.LabelFrame(main_container, text="Security", 
                                   font=("Consolas", 12, "bold"), bg="#282c34", fg="#61dafb", 
                                   padx=10, pady=10)
        pass_frame.pack(fill=tk.X)
        
        self.pass_entry = tk.Entry(pass_frame, show="•", font=("Consolas", 11), width=30, bg="#21252b", fg="#61dafb", insertbackground="#61dafb")
        self.pass_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Encode button
        encode_btn = tk.Button(main_container, text="Encode Message", command=self.encode_message, 
                               bg="#61dafb", fg="#282c34", font=("Consolas", 11, "bold"), 
                               padx=20, pady=10)
        encode_btn.pack()

    def select_image(self):
        self.img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if self.img_path:
            self.img_path_label.config(text=f"Selected: {os.path.basename(self.img_path)}")

    def generate_key(self, password):
        return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

    def encrypt_message(self, message, password):
        key = self.generate_key(password)
        cipher_suite = Fernet(key)
        encrypted_message = cipher_suite.encrypt(message.encode())
        return encrypted_message.decode('utf-8')

    def encode_message(self):
        if not self.img_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
            
        msg = self.msg_entry.get("1.0", tk.END).strip()
        password = self.pass_entry.get()
        
        if not msg or not password:
            messagebox.showerror("Error", "Please enter both message and password!")
            return
        
        # Encrypt the message
        try:
            encrypted_msg = self.encrypt_message(msg, password)
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
            return
        
        # Check if message is too long for the image
        try:
            img = cv2.imread(self.img_path)
            if img is None:
                raise Exception("Could not read image")
            
            max_bytes = img.shape[0] * img.shape[1] * 3 // 8
            if len(encrypted_msg) > max_bytes - 1:
                messagebox.showerror("Error", 
                    f"Message is too long! Maximum {max_bytes - 1} characters allowed for this image.")
                return
                
            # Store message length at the beginning
            msg_length = len(encrypted_msg)
            img[0, 0, 0] = msg_length
            
            # Encode message starting from second pixel
            n, m, z = 1, 0, 0
            for char in encrypted_msg:
                if n >= img.shape[0] or m >= img.shape[1]:
                    raise Exception("Image too small for the message")
                img[n, m, z] = self.char_to_int[char]
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                z = (z + 1) % 3
            
            # Save encoded image
            save_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                    filetypes=[("PNG files", "*.png")])
            if save_path:
                cv2.imwrite(save_path, img)
                messagebox.showinfo("Success", "Message encoded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()