import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from cryptography.fernet import Fernet
import hashlib
import base64
import os

class DecryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Decoding - Hacker Theme")
        self.root.geometry("600x400")
        self.root.configure(bg="#000000")  # Pure black background
        
        self.img_path = None
        self.int_to_char = {i: chr(i) for i in range(255)}
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme
        self.style.configure('Custom.TFrame', background='#000000')
        self.style.configure('Custom.TButton', padding=10, font=('Courier New', 12), background="#00ff00", foreground="#000000")
        self.style.configure('Custom.TLabel', background="#000000", foreground="#00ff00", font=('Courier New', 12))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root, style='Custom.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ttk.Frame(main_container, style='Custom.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(title_frame, text="Image Decoding", 
                         font=("Courier New", 20, "bold"), bg="#000000", fg="#00ff00")
        title.pack()
        
        # Image selection section
        img_frame = tk.LabelFrame(main_container, text="Image Selection", 
                                  font=("Courier New", 12, "bold"), bg="#000000", fg="#00ff00", 
                                  padx=10, pady=10)
        img_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.img_path_label = tk.Label(img_frame, text="No image selected", 
                                       bg="#000000", fg="#00ff00", wraplength=300)
        self.img_path_label.pack(fill=tk.X, pady=(0, 5))
        
        select_btn = tk.Button(img_frame, text="Select Image", command=self.select_image, 
                               bg="#00ff00", fg="#000000", font=("Courier New", 11), padx=20, pady=5)
        select_btn.pack()
        
        # Password section
        pass_frame = tk.LabelFrame(main_container, text="Security", 
                                   font=("Courier New", 12, "bold"), bg="#000000", fg="#00ff00", 
                                   padx=10, pady=10)
        pass_frame.pack(fill=tk.X)
        
        self.pass_entry = tk.Entry(pass_frame, show="•", font=("Courier New", 11), width=30, bg="#000000", fg="#00ff00", insertbackground="#00ff00")
        self.pass_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Decode button
        decode_btn = tk.Button(main_container, text="Decode Message", command=self.decode_message, 
                               bg="#00ff00", fg="#000000", font=("Courier New", 11, "bold"), 
                               padx=20, pady=10)
        decode_btn.pack()

        # Output section
        output_frame = tk.LabelFrame(main_container, text="Decoded Message", 
                                     font=("Courier New", 12, "bold"), bg="#000000", fg="#00ff00", 
                                     padx=10, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.decoded_text = tk.Text(output_frame, font=("Courier New", 11), wrap=tk.WORD, 
                                    bg="#000000", fg="#00ff00", insertbackground="#00ff00")
        self.decoded_text.pack(fill=tk.BOTH, expand=True)
        self.decoded_text.config(state=tk.DISABLED)

    def select_image(self):
        self.img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if self.img_path:
            self.img_path_label.config(text=f"Selected: {os.path.basename(self.img_path)}")

    def generate_key(self, password):
        return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

    def decrypt_message(self, encrypted_message, password):
        key = self.generate_key(password)
        cipher_suite = Fernet(key)
        decrypted_message = cipher_suite.decrypt(encrypted_message.encode()).decode()
        return decrypted_message

    def decode_message(self):
        if not self.img_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
            
        password = self.pass_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter the password!")
            return
            
        try:
            img = cv2.imread(self.img_path)
            if img is None:
                raise Exception("Could not read image")
                
            # Get message length from first pixel
            msg_length = int(img[0, 0, 0])
            
            # Decode message starting from second pixel
            message = ""
            n, m, z = 1, 0, 0
            for _ in range(msg_length):
                if n >= img.shape[0] or m >= img.shape[1]:
                    raise Exception("Message appears to be corrupted")
                message += self.int_to_char[int(img[n, m, z])]
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                z = (z + 1) % 3
            
            # Decrypt the message
            try:
                decrypted_msg = self.decrypt_message(message, password)
            except Exception as e:
                messagebox.showerror("Error", f"Decryption failed: {str(e)}")
                return
            
            # Update the text area with decoded message
            self.decoded_text.config(state=tk.NORMAL)
            self.decoded_text.delete(1.0, tk.END)
            self.decoded_text.insert(tk.END, decrypted_msg)
            self.decoded_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DecryptionApp(root)
    root.mainloop()