import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from lsb_utils import lsb_encode, lsb_decode
from edge_utils import detect_edges, edge_embed, edge_decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64, re, os

def clean_and_pad_b64(data: str) -> bytes:
    data = re.sub(r'[^A-Za-z0-9+/=]', '', data)
    rem = len(data) % 4
    if rem: data += "=" * (4 - rem)
    return data.encode('ascii')

class StegoApp(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Hybrid Steganography")
        self.geometry("800x600")
        self.minsize(700, 500)

        self.notebook = tb.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        self.build_encrypt_tab()
        self.build_decrypt_tab()

    def build_encrypt_tab(self):
        frame = tb.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text="🔒 Encrypt & Embed")

        tb.Button(frame, text="📁 Select Image", bootstyle=("info", "outline"),
                  command=self.select_encrypt_image).grid(row=0, column=0, sticky=W)
        self.enc_canvas = tb.Label(frame)
        self.enc_canvas.grid(row=1, column=0, columnspan=2, pady=10)

        tb.Label(frame, text="Secret Message:", font=("Arial", 11)).grid(row=2, column=0, sticky=W, pady=(10,0))
        self.enc_msg = tb.Entry(frame, width=50); self.enc_msg.grid(row=2, column=1, pady=(10,0))
        tb.Label(frame, text="Password:", font=("Arial", 11)).grid(row=3, column=0, sticky=W, pady=(10,0))
        self.enc_pw = tb.Entry(frame, show="*", width=50); self.enc_pw.grid(row=3, column=1, pady=(10,0))

        tb.Button(frame, text="🔐 Embed & Save", bootstyle="success", command=self.do_encrypt) \
          .grid(row=4, column=0, columnspan=2, pady=20, sticky="ew")

        frame.columnconfigure(1, weight=1)
        self.enc_img_path = None

    def select_encrypt_image(self):
        ft = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        path = filedialog.askopenfilename(filetypes=ft)
        if path:
            self.enc_img_path = path
            img = Image.open(path).convert("RGB").resize((300, 300))
            self.enc_photo = ImageTk.PhotoImage(img)
            self.enc_canvas.config(image=self.enc_photo)

    def do_encrypt(self):
        if not self.enc_img_path or not self.enc_msg.get() or not self.enc_pw.get():
            return messagebox.showerror("Error", "Please select an image, enter a message, and a password.")
        img = Image.open(self.enc_img_path).convert("RGB")
        key = PBKDF2(self.enc_pw.get(), b"salt", dkLen=32)
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(self.enc_msg.get().encode())
        payload = cipher.nonce + ciphertext + tag
        b64 = base64.b64encode(payload).decode()
        half = len(b64) // 2
        img2 = lsb_encode(img, b64[:half])
        img3 = edge_embed(img2, b64[half:], detect_edges(self.enc_img_path))
        out = os.path.splitext(os.path.basename(self.enc_img_path))[0] + "_stego.png"
        img3.save(out)
        messagebox.showinfo("Encrypted!", f"Saved stego image as:\n{out}")

    def build_decrypt_tab(self):
        frame = tb.Frame(self.notebook, padding=20)
        self.notebook.add(frame, text="🔓 Extract & Decrypt")

        tb.Button(frame, text="📁 Select Image", bootstyle=("info", "outline"),
                  command=self.select_decrypt_image).grid(row=0, column=0, sticky=W)
        self.dec_canvas = tb.Label(frame); self.dec_canvas.grid(row=1, column=0, columnspan=2, pady=10)

        tb.Label(frame, text="Password:", font=("Arial", 11)).grid(row=2, column=0, sticky=W)
        self.dec_pw = tb.Entry(frame, show="*", width=50); self.dec_pw.grid(row=2, column=1, pady=5)
        tb.Button(frame, text="🔍 Extract Message", bootstyle="info", command=self.do_decrypt) \
          .grid(row=3, column=0, columnspan=2, pady=20, sticky="ew")

        frame.columnconfigure(1, weight=1)
        self.dec_img_path = None

    def select_decrypt_image(self):
        ft = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        path = filedialog.askopenfilename(filetypes=ft)
        if path:
            self.dec_img_path = path
            img = Image.open(path).convert("RGB").resize((300, 300))
            self.dec_photo = ImageTk.PhotoImage(img)
            self.dec_canvas.config(image=self.dec_photo)

    def do_decrypt(self):
        if not self.dec_img_path or not self.dec_pw.get():
            return messagebox.showerror("Error", "Please select a stego image and enter the password.")
        img = Image.open(self.dec_img_path).convert("RGB")
        raw = lsb_decode(img) + edge_decode(img, detect_edges(self.dec_img_path))
        data = clean_and_pad_b64(raw)
        try:
            payload = base64.b64decode(data)
        except Exception:
            return messagebox.showerror("Error", "Invalid embedded data!")

        key = PBKDF2(self.dec_pw.get(), b"salt", dkLen=32)
        cipher = AES.new(key, AES.MODE_EAX, nonce=payload[:16])
        try:
            pt = cipher.decrypt_and_verify(payload[16:-16], payload[-16:])
            messagebox.showinfo("Decrypted Message", pt.decode())
        except ValueError:
            messagebox.showerror("Error", "Wrong password or corrupted data.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

if __name__ == "__main__":
    StegoApp().mainloop()
